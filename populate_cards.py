import requests, re, optparse, urls
from bs4 import BeautifulSoup
import sys

p = optparse.OptionParser()
p.add_option('--sid', '-s', default="")
p.add_option('--file', '-f', default="cards.tsv")
options, arguments = p.parse_args()

sys.stdout = open(options.file, 'w')

cookies = dict(sid=options.sid)
align_rgx = re.compile(r"(\d)")
prefix_rgx = re.compile(r"(^\[.*?\])\s")

print "global_id" + "\t" + "name" + "\t" + "name_id" + "\t" + "name_prefix" + "\t" + "image_id" + "\t" + "rarity" + "\t" + "alignment" + "\t" + "min_rarity" + "\t" + "base_id" + "\t" +  "desc" + "\t" + "base_atk" + "\t" + "base_def" + "\t" + "pwr_req" + "\t" + "gender" + "\t" + "faction" + "\t" + "silver" + "\t" + "ability" + "\t" + "usage" + "\t" + "effect" + "\t" + "max_level" + "\t" + "max_mastery"


for a in range(1,4):
	for br in range(0,6):
		for v in range(0,2):
			for id in range(1,26):
				rarity = str(int(br)+int(v))
				global_id = str(a)+rarity+str(br)+str(id).zfill(3)+str(v)
				archive_url = "http://ultimate-a.cygames.jp/ultimate/archive/view_other/00000001/"+global_id+"/0/1/0/0/0"
				rally_url = "http://ultimate-a.cygames.jp/ultimate/gacha/result/?t=1&c[0]="+global_id+"&s[0]=00000000001&f[0]=0&fid=0900_free_gacha.swf&effect=0&ticket_type=0&ticket_id=0&ticket_cost=0&rnd=951429010&flashParam=419722658&rnd=334048153&rnd=420997282"

				name = ""
				name_id = ""
				name_prefix = ""
				image_id = ""
				desc = ""
				base_atk = ""
				base_def = ""
				pwr_req = ""
				gender = ""
				faction = ""
				silver = ""
				ability = ""
				usage = ""
				effect = ""
				max_level = ""
				max_mastery = ""

				card_exists = False

				archive_request = requests.get(archive_url, cookies=cookies)
				if archive_request.status_code != 200:
					archive_soup = False
				else:
					archive_soup = BeautifulSoup(archive_request.text, "lxml")
					if archive_soup.select(".userLeft"):
						card_exists = True

						alignment = a
						min_rarity = br
						base_id = str(id).zfill(3).encode('utf-8')

						name = re.search(r"\W+\s+(.*?)\(", archive_soup.select(".window3")[0].get_text().encode('utf-8').strip()).group(1)
						name_id = name
						name_prefix_match = prefix_rgx.search(name)
						if name_prefix_match:
							name_prefix = name_prefix_match.group(1).encode('utf-8').strip()

						image_id = re.search(r"\/card\/\w+\/([a-f0-9]+)\.jpg", archive_soup.select(".window3Text img")[0].get("src").encode('utf-8').strip()).group(1)
						desc = archive_soup.select(".window3Text p")[0].get_text().encode('utf-8').strip()
						base_atk = re.search(r"ATK:\s(\d+)", archive_soup.select(".userLeft p")[0].get_text().encode('utf-8').strip()).group(1)
						base_def = re.search(r"DEF:\s(\d+)", archive_soup.select(".userLeft p")[0].get_text().encode('utf-8').strip()).group(1)
						pwr_req = re.search(r"PWR REQ:\s(\d+)", archive_soup.select(".userLeft p")[0].get_text().encode('utf-8').strip()).group(1)
						gender = re.search(r"Gender:\s(\w)", archive_soup.select(".userLeft p")[1].get_text().encode('utf-8').strip()).group(1)
						faction = re.search(r"Faction:\s([\w\d]+)", archive_soup.select(".userLeft p")[1].get_text().encode('utf-8').strip()).group(1)
						silver = re.search(r"Sale Price:\s([,\d]+)",archive_soup.find(text=re.compile(r"Sale Price:")).find_parent("div").get_text().encode('utf-8').strip()).group(1).replace(",", "")

						ability_found = archive_soup.find(text=re.compile(r"Ability:"))
						if ability_found:
							ability_match = re.search(r"Ability:\s([\w\s]+)Usage",ability_found.find_parent("div").get_text().encode('utf-8').strip())
							if ability_match:
								ability = ability_match.group(1).encode('utf-8').strip()

								usage_found = archive_soup.find(text=re.compile(r"Usage:"))
								if usage_found:
									usage_match = re.search(r"Usage:\s([\w\s]+)Effect",usage_found.find_parent("table").get_text().strip())
									if usage_match:
										usage = usage_match.group(1).encode('utf-8').strip()

								effect_found = archive_soup.find_all(text=re.compile("Effect:"), name='td')								
								if effect_found:
									for effect_item in effect_found:
										for effect_sibling in effect_item.find_parent("table").find_all("td"):
											if effect_sibling.name == "td":
												effect_match = effect_sibling.string
												if effect_match:
													effect = unicode(effect_match).encode('utf-8').strip()

				rally_request = requests.get(rally_url, cookies=cookies)
				if rally_request.status_code != 200:
					rally_soup = False
				else:
					rally_soup = BeautifulSoup(rally_request.text, "lxml")
					if rally_soup.select(".userLeft"):
						rally_found = rally_soup.select(".userLeft p")[0]
						if rally_found:
							max_level_match = re.search(r"Lv:\s?\d+\/(\d+)", rally_found.get_text().encode('utf-8').strip())
							if max_level_match:
								max_level = re.search(r"Lv:\s?\d+\/(\d+)", rally_found.get_text().encode('utf-8').strip()).group(1)

							max_mastery_match = re.search(r"Mastery:\s?\d+\/(\d+)", rally_found.get_text().encode('utf-8').strip())
							if max_mastery_match:
								max_mastery = max_mastery_match.group(1)

				if card_exists:
					print global_id + "\t" + name + "\t" + name_id + "\t" + name_prefix + "\t" + image_id + "\t" + rarity + "\t" + alignment + "\t" + min_rarity + "\t" + base_id + "\t" + desc + "\t" + base_atk + "\t" + base_def + "\t" + pwr_req + "\t" + gender + "\t" + faction + "\t" + silver + "\t" + ability + "\t" + usage + "\t" + effect + "\t" + max_level + "\t" + max_mastery
