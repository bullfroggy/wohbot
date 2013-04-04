import requests, re, optparse
import itertools
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
 
known_globals = ["1000010","1000020","1000030","1000040","1000050","1000060","1000070","1000080","1000090","1000100","1000110","1000120","1000130","1100011","1100021","1100031","1100041","1100051","1100061","1100071","1100081","1100091","1100101","1100111","1100121","1100131","1110010","1110020","1110030","1110040","1110050","1110060","1110070","1110080","1110090","1110100","1110110","1110120","1210011","1210021","1210031","1210041","1210051","1210061","1210071","1210081","1210091","1210101","1210111","1210121","1220010","1220020","1220030","1220040","1220050","1220060","1220070","1220080","1220090","1220100","1220110","1220120","1220130","1220140","1220150","1220160","1220170","1220180","1220190","1220200","1220210","1220220","1220230","1220240","1220260","1220270","1220280","1320011","1320021","1320031","1320041","1320051","1320061","1320071","1320081","1320091","1320111","1320121","1320131","1320141","1320151","1320161","1320171","1320181","1320191","1320201","1320211","1320221","1320231","1320241","1320261","1320271","1320281","1330010","1330020","1330030","1330040","1330050","1330060","1330070","1330080","1330090","1330100","1330110","1330120","1330130","1330150","1420092","1430011","1430021","1430031","1430041","1430051","1430061","1430071","1430081","1430091","1430101","1430111","1430121","1430131","1430151","1440010","1440020","1440030","1440040","1440050","1440060","1440070","1440080","1440090","1440100","1440120","1440130","1440140","1520093","1540011","1540021","1540031","1540041","1540051","1540061","1540071","1540081","1540091","1540101","1540121","1540131","1540141","1550010","1550020","1650011","1650021","2000010","2000020","2000030","2000040","2000050","2000060","2000070","2000080","2000090","2000100","2000110","2000120","2000130","2100011","2100021","2100031","2100041","2100051","2100061","2100071","2100081","2100091","2100101","2100111","2100121","2100131","2110010","2110020","2110030","2110040","2110050","2110060","2110070","2110080","2110090","2110110","2110120","2210011","2210021","2210031","2210041","2210051","2210061","2210071","2210081","2210091","2210111","2210121","2220010","2220020","2220030","2220040","2220050","2220060","2220070","2220080","2220090","2220100","2220110","2220120","2220130","2220140","2220150","2220160","2220170","2220180","2320011","2320021","2320031","2320041","2320051","2320061","2320071","2320081","2320101","2320111","2320121","2320131","2320141","2320151","2320161","2320171","2320181","2330010","2330020","2330030","2330040","2330050","2330060","2330070","2330080","2330090","2330100","2330110","2330120","2330130","2330140","2330150","2330160","2330170","2330180","2330190","2420122","2430011","2430021","2430031","2430041","2430051","2430061","2430071","2430081","2430091","2430101","2430111","2430121","2430131","2430141","2430151","2430161","2430171","2430181","2430191","2440010","2440020","2440030","2440040","2440050","2440060","2440070","2440080","2440090","2440100","2440110","2440120","2440130","2440140","2440150","2520123","2540011","2540021","2540031","2540041","2540051","2540061","2540071","2540081","2540091","2540101","2540111","2540121","2540131","2540141","2540151","2550010","2550020","2550030","2550040","2550050","2650011","2650021","2650031","2650041","2650051","3000010","3000020","3000030","3000040","3000050","3000060","3000070","3000080","3000090","3000100","3000110","3000120","3000130","3100011","3100021","3100031","3100041","3100051","3100061","3100071","3100081","3100091","3100101","3100111","3100121","3100131","3110010","3110020","3110030","3110040","3110050","3110060","3110070","3110080","3110090","3110110","3110120","3210011","3210021","3210031","3210041","3210051","3210061","3210071","3210081","3210091","3210111","3210121","3220010","3220020","3220030","3220040","3220050","3220060","3220070","3220080","3220090","3220100","3220110","3220120","3220130","3220140","3220150","3220160","3220170","3220180","3220190","3220200","3320011","3320021","3320031","3320041","3320051","3320061","3320071","3320081","3320101","3320111","3320121","3320131","3320141","3320151","3320161","3320171","3320181","3320191","3320201","3330010","3330020","3330030","3330040","3330050","3330060","3330070","3330080","3330100","3330110","3330120","3330130","3330140","3330150","3330160","3330170","3330180","3330190","3330200","3330210","3330220","3420162","3430011","3430021","3430031","3430041","3430051","3430061","3430071","3430081","3430101","3430111","3430121","3430131","3430141","3430151","3430161","3430171","3430181","3430191","3430201","3430211","3430221","3440010","3440020","3440030","3440040","3440050","3440060","3440070","3440080","3440090","3440100","3440110","3440120","3520163","3540011","3540021","3540031","3540041","3540051","3540061","3540071","3540081","3540091","3540101","3540111","3540121","3550010","3550020","3550030","3550040","3550050","3650011","3650021","3650031","3650041","3650051"]
 
 
def split_global_id(id):
    """
    Split an id into its component parts, returning a tuple containing the
    elements.
    """
    a = id[:1]
    rarity = id[1:2]
    br = id[2:3]
    b_id = id[3:6]
    v = id[-1]
    return a, rarity, br, b_id, v
 
 
def fetch_url(url):
    """
    Fetch the given URL, raising an error for a non-200 status code.
    """
    req = requests.get(url, cookies=cookies)
    req.raise_for_status()
    return req
 
 
def process_parent(card_id):
    sibling_count = parse_card(card_id)
    if sibling_count > 1:
        a, rarity, br, id, vp = split_global_id(card_id)
        siblings = [a + str(int(br) + v) + br + id + str(v) for v in range(1, sibling_count)]
        process_siblings(siblings)
 
 
def process_siblings(siblings):
    # Process the list of sibling cards
    for sibling in siblings:
        parse_card(sibling)
 
 
def parse_card(global_id):
    a, rarity, br, id, v = split_global_id(global_id)
 
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
 
    v_count = 0
    card_exists = False
 
    try:
        archive_request = fetch_url(archive_url)
    except requests.exceptions.HTTPError:
        archive_soup = False
    else:
        archive_soup = BeautifulSoup(archive_request.text, "lxml")
 
    if archive_soup and archive_soup.select(".userLeft"):
 
        card_exists = True

        v_count = len(archive_soup.select(".space1emBT td"))
 
        alignment = str(a).encode('utf-8')
        min_rarity = str(br).encode('utf-8')
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
 
    try:
        rally_request = fetch_url(rally_url)
    except requests.exceptions.HTTPError:
        rally_soup = False
    else:
        rally_soup = BeautifulSoup(rally_request.text, "lxml")
 
    if rally_soup and rally_soup.select(".userLeft"):
        rally_found = rally_soup.select(".userLeft p")[0]
        if rally_found:
            max_level_match = re.search(r"Lv:\s?\d+\/(\d+)", rally_found.get_text().encode('utf-8').strip())
            if max_level_match:
                max_level = re.search(r"Lv:\s?\d+\/(\d+)", rally_found.get_text().encode('utf-8').strip()).group(1)
 
            max_mastery_match = re.search(r"Mastery:\s?\d+\/(\d+)", rally_found.get_text().encode('utf-8').strip())
            if max_mastery_match:
                max_mastery = max_mastery_match.group(1)
 
    if card_exists:
        print '\t'.join([global_id, name, name_id, name_prefix, image_id, rarity, alignment, min_rarity, base_id, v, desc, base_atk, base_def, pwr_req, gender, faction, silver, ability, usage, effect, max_level, max_mastery])
    elif archive_soup and not card_exists:
        #print '\t'.join([global_id, "Does Not Exist"])
        pass
    else:
        print '\t'.join([global_id, "Error Fetching Card Archive URL"])
 
    return v_count
 
 
if __name__ == "__main__":
    print '\t'.join(["global_id", "name", "name_id", "name_prefix", "image_id", "rarity", "alignment", "min_rarity", "base_id", "version", "desc", "base_atk", "base_def", "pwr_req", "gender", "faction", "silver", "ability", "usage", "effect", "max_level", "max_mastery"])
 
    for id in list(itertools.product(range(1, 4),
                                     range(0, 6),
                                     range(1, 32))):
        global_id = str(id[0]) + str(id[1]) * 2 + str(id[2]).zfill(3) + '0'
        if global_id not in known_globals:
            process_parent(global_id)