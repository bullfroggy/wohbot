import requests, re, optparse, urls
from bs4 import BeautifulSoup

p = optparse.OptionParser()
p.add_option('--sid', '-s', default="")
options, arguments = p.parse_args()


cookies = dict(sid=options.sid)

for a in range(1,4):
	for br in range(0,6):
		for v in range(0,2):
			for id in range(1,26):
				global_id = str(a)+str(int(br)+int(v))+str(br)+str(id).zfill(3)+str(v)
				url = "http://ultimate-a.cygames.jp/ultimate/archive/view_other/00000001/"+global_id+"/0/1/0/0/0"

				r = requests.get(url, cookies=cookies)
				if r.status_code != 200:
					soup = False
				else:
					soup = BeautifulSoup(r.text)
					if len(soup.select(".window3Text")) > 0:
						"""
						Base ID
						Name Prefix
						Name ID
						Gender
						Alignment
						Faction
						Ability
						Usage
						Min Rarity

						base_card
						rarity
					-	description
						sell price
						power req
						base atk
						base def
					-	image id 
						Global ID
						"""
						image_id = re.search(r"\/card\/\w+\/([a-f0-9]+)\.jpg", soup.select(".window3Text img")[0].get("src").strip()).group(1)
						desc = soup.select(".window3Text p")[0].get_text().strip()
						base_atk = soup.findAllByRE(r"ATK:\s+(\d+)").get_text().strip()
						print global_id + " | " + base_atk
						"""
						Base ATK: (".userLeft p:first") ATK:\s(\d+)
						Base DEF: (".userLeft p:first") DEF:\s(\d+)
						Power REQ: (".userLeft p:first") PWR\sREQ:\s(\d+)
						Gender: (".userLeft p:second") Gender:\s(\w+)
						Faction: (".userLeft p:second") Faction:\s(\.+)
						Ability: (".userLeft p:third") Ability:\w(\.+)
						Usage: (".userLeft table tbody tr:first td:second")
						Effect: (".userLeft table tbody tr:second td:second")
						Sell Price:
						Alignment:
						"""