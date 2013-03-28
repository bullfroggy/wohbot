import urls, requests, re
from bs4 import BeautifulSoup
from card import Card

class Player:
	settings = {
				"sid": "",
				"name": "",
				"level": 0,
				"farm_mission": urls.MISSION_2_3,

			}

	def __init__(self, settings):
		self.settings.update(settings)
		self.catalog = [] # populate via update_cards method
		self.presents = []
		self.device_presents = []
		self.pending_trades = []
	
	def get_farm_url(self):
		if self.settings["farm_mission"]:
			return self.settings["farm_mission"]
		else:
			return False
	
	def get_card_count(self):
		html = self.parse_page(urls.MYPAGE)
		if html:
			card_text = html.select(".card a")[0].get_text().strip()
			current_card_count = int(re.match(r"\d+", card_text).group())
			return int(re.match(r"\d+", card_text).group())
		else:
			return 0

	def update_cards(self):
		new_roster = []
		card_list_urls = [urls.CARD_LIST_INDEX+str(page) for page in range(0, self.get_card_count(), 10)]
		for url in card_list_urls:
			print "Walking " + url + "..."
			html = self.parse_page(url)
			if html:
				page_cards = html.select("a[href^="+urls.CARD_LIST_DESC+"]")
				#page_cards = html.select(".member_bg>div+table~table")
				
				for card in page_cards:
					unique_id = re.search(r"desc\/(\d+)", card.get("href")).group(1)
					if(unique_id):
						middle_element = card.findParent("table")
						top_element = middle_element.findPreviousSibling("div")
						bottom_element = middle_element.findNextSibling("table")
						#print top_element
						rarity = re.search(r"\((\w+)\)", str(top_element.find("p"))).group(1)
						print rarity
						alignment = re.search(r"(\W+)", str(top_element.find("span"))).group(1)

						properties = {
							"rarity": rarity,
							"alignment": alignment,

						}
						#curr_card = 

						#print curr_card.get_unique_id()
						
						new_roster.append(Card(unique_id, properties))

		new_roster = list(set(new_roster))

		for each_card in new_roster:
			print each_card.get_alignment() 

		return 

	def get_all_cards(self)
		card_urls = ["http://ultimate-a.cygames.jp/ultimate/archive/view_other/00000001/"+str(page)+"/0/1/0/0/0" for page in range(0, self.get_card_count(), 10)]



	def get_sid(self):
		return self.settings["sid"]

	def set_farm_mission(self, farm_mission):
		self.farm_mission = farm_mission

	def get_farm_mission(self):
		return self.farm_mission

	def parse_page(self, url):
		cookies = dict(sid=self.get_sid())
		r = requests.get(url, cookies=cookies)
		if r.status_code == 200:
			return BeautifulSoup(r.text)
		else:
			return False

	def get_card_space_remaining(self):
		html = self.parse_page(urls.MYPAGE)
		if html:
			card_text = html.select(".card a")[0].get_text().strip()
			current_card_count = int(re.match(r"\d+", card_text).group())
			return int(re.search(r"\/(\d+)", card_text).group(1)) - int(re.match(r"\d+", card_text).group())

	def get_remaining_energy(self):
		html = self.parse_page(urls.MYPAGE)
		if html:
			energy_text = html.select(".EnergyPowerTxt")[0].get_text()
			return int(re.match(r"\d+", energy_text).group())
		else:
			return False

	def get_remaining_silver(self):
		html = self.parse_page(urls.MYPAGE)
		if html:
			return int(html.select(".silver")[0].get_text().strip().replace(',', ''))
		else:
			return False

	def farm(self, iterations):
		mission_url = self.get_farm_url()

		print "Running the farm %s times." % iterations
		if self.parse_page(mission_url):
			for x in range(0, iterations - 1):
				self.parse_page(mission_url)
		else:
			return False

		return True

	def max_farm(self):
		required_battles = int(self.get_remaining_energy() / 3)
		self.farm(required_battles)

	def get_remaining_atk_power(self):
		html = self.parse_page(urls.MYPAGE)
		if html:
			atk_text = html.select(".AttackPowerTxt")[0].get_text()
			return int(re.match(r"\d+", atk_text).group())
		else:
			return False
	
