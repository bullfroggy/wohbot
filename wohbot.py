import requests, re, optparse
from bs4 import BeautifulSoup

class Bot:
	settings = {
				"sid": "",
				"farm_mission": "23",
				"urls": {
					"mypage": "http://ultimate-a.cygames.jp/ultimate/mypage/index",
					"fusion": "http://ultimate-a.cygames.jp/ultimate/card_union",
					"mission-23": "http://ultimate-a.cygames.jp/ultimate/quest/play/2/3",
					"mission-24": "http://ultimate-a.cygames.jp/ultimate/quest/play/2/4",
				}
			}

	def __init__(self, settings):
		self.settings.update(settings)

	def getURL(self, url):
		if self.settings["urls"][url]:
			return self.settings["urls"][url]
		else:
			return False


	def getSID(self):
		return self.settings["sid"]

	def setFarmMission(self, farm_mission):
		self.farm_mission = farm_mission

	def getFarmMission(self):
		return self.farm_mission

	def parsePage(self, url):
		cookies = dict(sid=self.getSID())
		r = requests.get(url, cookies=cookies)
		if r.status_code == 200:
			return BeautifulSoup(r.text)
		else:
			return False

	def getCardSpaceRemaining(self):
		mypage_url = self.getURL("mypage")
		html = self.prasePage(mypage_url)
		if html:
			card_text = html.select(".card a")[0].get_text().strip()
			current_card_count = int(re.match(r"\d+", card_text).group())
			return int(re.search(r"\/(\d+)", card_text).group(1)) - int(re.match(r"\d+", card_text).group())

	def getRemainingEnergy(self):
		mypage_url = self.getURL("mypage")
		html = self.parsePage(mypage_url)
		if html:
			energy_text = html.select(".EnergyPowerTxt")[0].get_text()
			return int(re.match(r"\d+", energy_text).group())
		else:
			return False

	def getRemainingATKPower(self):
		mypage_url = self.getURL("mypage")
		html = self.parsePage(mypage_url)
		if html:
			atk_text = html.select(".AttackPowerTxt")[0].get_text()
			return int(re.match(r"\d+", atk_text).group())
		else:
			return False

	def farm(self, iterations):
		mission_url = self.getURL("mission-%s" %self.settings["farm_mission"])

		print "Running the farm %s times." % iterations
		if self.parsePage(mission_url):
			for x in range(0, iterations - 1):
				self.parsePage(mission_url)
		else:
			return False

		return True

	def maxFarm(self):
		required_battles = int(self.getRemainingEnergy() / 3)
		self.farm(required_battles)

def main():
	p = optparse.OptionParser()
	p.add_option('--sid', '-s', default="")
	p.add_option('--farm_mission', '-f', default="23")
	options, arguments = p.parse_args()
	settings = {
		"sid": options.sid,
		"farm_mission": options.farm_mission,
	}
	bot = Bot(settings)
	bot.maxFarm()
	# Adding a second maxFarm to catch the Levelups.  Should be done better at a later time
	bot.maxFarm()
	print "Done!"

if __name__ == '__main__':
       main()
