# coding: utf-8
from __future__ import print_function
import requests, re, optparse
import itertools
from bs4 import BeautifulSoup
import sys
 
p = optparse.OptionParser()
p.add_option('--sid', '-s', default="")
p.add_option('--file', '-f', default="cards.tsv")
options, arguments = p.parse_args()
 
f = open(options.file, 'w')
 
cookies = dict(sid=options.sid)
NBSP = u"\xc2"

name_rgx = re.compile(r"\W+\s+([\[\]\w\d\s\n\-.]*\+*)\(")
align_rgx = re.compile(r"(\d)")
prefix_rgx = re.compile(r"(^\[.*?\])\s(.*)")
eff_strength_rgx = re.compile(r"(Partially|Notably|Significantly|Remarkably|Extremely)")
eff_cards_rgx = re.compile(r"(Speeds|Bruisers|Tactics|self|team)")
eff_attr_rgx = re.compile(r"(ATK\/DEF|DEF|ATK)")
eff_play_self_rgx = re.compile(r"your|self")
eff_play_opp_rgx = re.compile(r"opposing")
eff_dir_up_rgx = re.compile(r"strengthen|raise|harden")
eff_dir_down_rgx = re.compile(r"weaken|degrade|lower")

# Cards in known_globals will be skipped from being parsed 
known_globals = ["3430091","1000010","1100011","1000020","1100021","1000030","1100031","1000040","1100041","1000050","1100051","1000060","1100061","1000070","1100071","1000080","1100081","1000090","1100091","1000100","1100101","1000110","1100111","1000120","1100121","1000130","1100131","1110010","1210011","1110020","1210021","1110030","1210031","1110040","1210041","1110050","1210051","1110060","1210061","1110070","1210071","1110080","1210081","1110090","1210091","1110100","1210101","1110110","1210111","1110120","1210121","1220010","1320011","1220020","1320021","1220030","1320031","1220040","1320041","1220050","1320051","1220060","1320061","1220070","1320071","1220080","1320081","1220090","1320091","1420092","1520093","1220100","1220110","1320111","1220120","1320121","1220130","1320131","1220140","1320141","1220150","1320151","1220160","1320161","1220170","1320171","1220180","1320181","1220190","1320191","1220200","1320201","1220210","1320211","1220220","1320221","1220230","1320231","1220240","1320241","1220260","1320261","1220270","1320271","1220280","1320281","1330010","1430011","1330020","1430021","1330030","1430031","1330040","1430041","1330050","1430051","1330060","1430061","1330070","1430071","1330080","1430081","1330090","1430091","1330100","1430101","1330110","1430111","1330120","1430121","1330130","1430131","1330150","1430151","1440010","1540011","1440020","1540021","1440030","1540031","1440040","1540041","1440050","1540051","1440060","1540061","1440070","1540071","1440080","1540081","1440090","1540091","1440100","1540101","1440120","1540121","1440130","1540131","1440140","1540141","1550010","1650011","1550020","1650021","2000010","2100011","2000020","2100021","2000030","2100031","2000040","2100041","2000050","2100051","2000060","2100061","2000070","2100071","2000080","2100081","2000090","2100091","2000100","2100101","2000110","2100111","2000120","2100121","2000130","2100131","2110010","2210011","2110020","2210021","2110030","2210031","2110040","2210041","2110050","2210051","2110060","2210061","2110070","2210071","2110080","2210081","2110090","2210091","2110110","2210111","2110120","2210121","2220010","2320011","2220020","2320021","2220030","2320031","2220040","2320041","2220050","2320051","2220060","2320061","2220070","2320071","2220080","2320081","2220090","2220100","2320101","2220110","2320111","2220120","2320121","2420122","2520123","2220130","2320131","2220140","2320141","2220150","2320151","2220160","2320161","2220170","2320171","2220180","2320181","2330010","2430011","2330020","2430021","2330030","2430031","2330040","2430041","2330050","2430051","2330060","2430061","2330070","2430071","2330080","2430081","2330090","2430091","2330100","2430101","2330110","2430111","2330120","2430121","2330130","2430131","2330140","2430141","2330150","2430151","2330160","2430161","2330170","2430171","2330180","2430181","2330190","2430191","2440010","2540011","2440020","2540021","2440030","2540031","2440040","2540041","2440050","2540051","2440060","2540061","2440070","2540071","2440080","2540081","2440090","2540091","2440100","2540101","2440110","2540111","2440120","2540121","2440130","2540131","2440140","2540141","2440150","2540151","2550010","2650011","2550020","2650021","2550030","2650031","2550040","2650041","2550050","2650051","3000010","3100011","3000020","3100021","3000030","3100031","3000040","3100041","3000050","3100051","3000060","3100061","3000070","3100071","3000080","3100081","3000090","3100091","3000100","3100101","3000110","3100111","3000120","3100121","3000130","3100131","3110010","3210011","3110020","3210021","3110030","3210031","3110040","3210041","3110050","3210051","3110060","3210061","3110070","3210071","3110080","3210081","3110090","3210091","3110110","3210111","3110120","3210121","3220010","3320011","3220020","3320021","3220030","3320031","3220040","3320041","3220050","3320051","3220060","3320061","3220070","3320071","3220080","3320081","3220090","3220100","3320101","3220110","3320111","3220120","3320121","3220130","3320131","3220140","3320141","3220150","3320151","3220160","3320161","3420162","3520163","3220170","3320171","3220180","3320181","3220190","3320191","3220200","3320201","3330010","3430011","3330020","3430021","3330030","3430031","3330040","3430041","3330050","3430051","3330060","3430061","3330070","3430071","3330080","3430081","3330100","3430101","3330110","3430111","3330120","3430121","3330130","3430131","3330140","3430141","3330150","3430151","3330160","3430161","3330170","3430171","3330180","3430181","3330190","3430191","3330200","3430201","3330210","3430211","3330220","3430221","3440010","3540011","3440020","3540021","3440030","3540031","3440040","3540041","3440050","3540051","3440060","3540061","3440070","3540071","3440080","3540081","3440090","3540091","3440100","3540101","3440110","3540111","3440120","3540121","3550010","3650011","3550020","3650021","3550030","3650031","3550040","3650041","3550050","3650051"]

# Remove following comment to parse all cards in sequence
#known_globals = [] 

# Cards in special_globals will be included though the generated sequence would not include them
# special_globals also appearing in known_globals will not be parsed 
special_globals = [3430091]

def to_unicode_or_bust(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj

def print_debug(obj):
    print(str(obj).encode('utf-8'))
    return

def decode_rarity(r_id):
    return (["Common", "Uncommon", "Rare", "S Rare", "SS Rare", "U Rare", "Legendary"])[int(r_id)]

def split_global_id(id):
    """
    Split an id into its component parts, returning a tuple containing the
    elements.
    """
    a = str(id)[:1]
    rarity = str(id)[1:2]
    br = str(id)[2:3]
    b_id = str(id)[3:6]
    v = str(id)[-1]
    return a, rarity, br, b_id, v
 
 
def fetch_url(url):
    """
    Fetch the given URL, raising an error for a non-200 status code.
    """
    req = requests.get(url, cookies=cookies)
    req.raise_for_status()
    return to_unicode_or_bust(req)
 
 
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
 
 
def parse_card(param_id):
    global_id = str(param_id)
    a, rarity, br, id, v = split_global_id(global_id)
 
    archive_url = "http://ultimate-a.cygames.jp/ultimate/archive/view_other/00000001/"+global_id+"/0/1/0/0/0"
    rally_url = "http://ultimate-a.cygames.jp/ultimate/gacha/result/?t=1&c[0]="+global_id+"&s[0]=00000000001&f[0]=0&fid=0900_free_gacha.swf&effect=0&ticket_type=0&ticket_id=0&ticket_cost=0&rnd=951429010&flashParam=419722658&rnd=334048153&rnd=420997282"
 
    name = ""
    name_id = ""
    name_prefix = ""
    root_name = ""
    image_id = ""
    desc = ""
    base_atk = ""
    base_def = ""
    pwr_req = ""
    gender = ""
    faction = ""
    silver = ""
    max_level = ""
    max_mastery = ""
    ability = ""
    usage = ""
    effect = ""
    effect_strength = ""
    effect_cards_affected = ""
    effect_attribute = ""
    effect_player = ""
    effect_direction = ""
 
    v_count = 0
    card_exists = False
 
    try:
        archive_request = fetch_url(archive_url)
    except requests.exceptions.HTTPError:
        archive_soup = False
    else:
        archive_soup = BeautifulSoup(archive_request.text, "lxml")
 
    if archive_soup and archive_soup.select(".userLeft") and archive_soup.select(".window3"):
 
        card_exists = True

        v_count = len(archive_soup.select(".space1emBT td"))
 
        alignment = str(a)
        min_rarity = str(br)
        base_id = str(id).zfill(3)

        #print(repr(archive_soup.select(".window3")[0].find(text="(").get_text()))
        name = re.search(r"\W+\s+(.*?).\(", archive_soup.select(".window3")[0].get_text().strip()).group(1)
        name_prefix_match = prefix_rgx.search(name)
        if name_prefix_match:
            name_prefix = name_prefix_match.group(1).strip()
            root_name = name_prefix_match.group(2).strip().lower().replace(" ", "")
            name_prefix = re.search(r"\[(.*)\]", name_prefix).group(1)
        else:
            root_name = re.search(r"([\w\d\s\n-\.]*)\+*", name).group(1).lower().replace(" ", "")
        root_name = re.search(r"(.*?)\+*$", root_name).group(1)

        print_debug("Found \"" + name + "\" (" + decode_rarity(rarity) + ")")
 
        image_id = re.search(r"\/card\/\w+\/([a-f0-9]+)\.jpg", archive_soup.select(".window3Text img")[0].get("src").strip()).group(1)
        desc = archive_soup.select(".window3Text p")[0].get_text().strip()
        base_atk = re.search(r"ATK:\s(\d+)", archive_soup.select(".userLeft p")[0].get_text().strip()).group(1)
        base_def = re.search(r"DEF:\s(\d+)", archive_soup.select(".userLeft p")[0].get_text().strip()).group(1)
        pwr_req = re.search(r"PWR REQ:\s(\d+)", archive_soup.select(".userLeft p")[0].get_text().strip()).group(1)
        gender = re.search(r"Gender:\s(\w)", archive_soup.select(".userLeft p")[1].get_text().strip()).group(1)
        faction = re.search(r"Faction:\s([\w\d\s]+)", archive_soup.select(".userLeft p")[1].get_text().strip()).group(1)
        silver = re.search(r"Sale Price:\s([,\d]+)",archive_soup.find(text=re.compile(r"Sale Price:")).find_parent("div").get_text().strip()).group(1).replace(",", "")
 
        ability_found = archive_soup.find(text=re.compile(r"Ability:"))
        if ability_found:
            #print_debug(ability_found.find_parent("div").get_text().strip())
            ability_match = re.search(r"Ability:\s([\w\s]+)Usage", ability_found.find_parent("div").get_text().strip())
            if ability_match:
                #print_debug("Found an ability named")
                ability = ability_match.group(1).strip()
                #print_debug(ability)
                usage_found = archive_soup.find(text=re.compile(r"Usage:"))
                if usage_found:
                    #print_debug("Found a usage of")
                    usage_match = re.search(r"Usage:\s([\w\s]+)Effect",usage_found.find_parent("table").get_text().strip())
                    if usage_match:
                        usage = usage_match.group(1).strip()
                        #print_debug(usage)
                effect_found = archive_soup.find_all(text=re.compile(r"Effect:"), name='td')                                
                if effect_found:
                    #print_debug("Found effect of")
                    effect_sibling = effect_found[0].find_next_sibling("td")
                    #print_debug(effect_sibling.string)
                    effect_match = effect_sibling.string
                    if effect_match:
                    #    print_debug(effect_match)
                        effect = effect_match.strip()

                        #parse out effect properties from effect verbiage
                        if eff_strength_rgx.search(effect):
                            effect_strength = eff_strength_rgx.search(effect).group(1)
                        if eff_cards_rgx.search(effect):
                            effect_cards_affected = eff_cards_rgx.search(effect).group(1)
                        if eff_attr_rgx.search(effect):
                            effect_attribute = eff_attr_rgx.search(effect).group(1)

                        if eff_play_self_rgx.search(effect):
                            effect_player = "self"
                        elif eff_play_opp_rgx.search(effect):
                            effect_player = "opponent"
                        else:
                            effect_player = "unknown"
                        
                        if eff_dir_up_rgx.search(effect):
                            effect_direction = "up"
                        elif eff_dir_down_rgx.search(effect):
                            effect_direction = "down"
                        else:
                            effect_direction = "unknown"

 
    try:
        rally_request = fetch_url(rally_url)
    except requests.exceptions.HTTPError:
        rally_soup = False
    else:
        rally_soup = BeautifulSoup(rally_request.text)
 
    if rally_soup and rally_soup.select(".userLeft"):
        rally_found = rally_soup.select(".userLeft p")[0]
        if rally_found:
            max_level_match = re.search(r"Lv:\s?\d+\/(\d+)", rally_found.get_text().strip())
            if max_level_match:
                max_level = re.search(r"Lv:\s?\d+\/(\d+)", rally_found.get_text().strip()).group(1)
 
            max_mastery_match = re.search(r"Mastery:\s?\d+\/(\d+)", rally_found.get_text().strip())
            if max_mastery_match:
                max_mastery = max_mastery_match.group(1)
 
    if card_exists and archive_soup and rally_soup:
        str_join = '\t'.join([global_id, name, name_prefix, root_name, image_id, rarity, alignment, min_rarity, base_id, v, desc, base_atk, base_def, pwr_req, gender, faction, silver, max_level, max_mastery,  ability, usage, effect, effect_strength, effect_cards_affected, effect_attribute, effect_player, effect_direction])
        str_join = str_join.encode('utf-8')
        print(str_join, file=f)
    elif archive_soup and not card_exists:
        #print('\t'.join([global_id, "Error: Card Does Not Exist"]))
        pass
    elif archive_soup and not rally_soup:
        print('\t'.join([global_id, "Error: Failed Fetching Card Rally URL"]))
    else:
        print('\t'.join([global_id, "Error: Failed Fetching Card Archive URL"]))
 
    return v_count
 
 
if __name__ == "__main__":
    print('\t'.join(["global_id (0)", "name (1)", "name_prefix (2)", "root_name (3)", "image_id (4)", "rarity (5)", "alignment (6)", "min_rarity (7)", "base_id (8)", "version (9)", "desc (10)", "base_atk (11)", "base_def (12)", "pwr_req (13)", "gender (14)", "faction (15)", "silver (16)", "max_level (17)", "max_mastery (18)", "ability (19)", "usage (20)", "effect_verbiage (21)", "effect_strength (22)", "effect_cards_affected (23)", "effect_attribute (24)", "effect_player (25)", "effect_direction (26)"]), file=f)
 
    # Check globals based upon a sequence of generated numbers
    for id in list(itertools.product(range(1, 4),
                                     range(0, 6),
                                     range(1, 32))):
        global_id = str(id[0]) + str(id[1]) * 2 + str(id[2]).zfill(3) + '0'
        if global_id not in known_globals:
            process_parent(global_id)

    # Check any special globals separate from generated list
    for id in special_globals:
        if id not in known_globals:
            process_parent(id)

    f.close()