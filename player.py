import re, copy
from card import Card
from woh import WoH

class Player(object):
    settings = {
        "sid": "",
        "name": "",
        "level": 0,
        "farm_mission": "",

    }

    def __init__(self, settings):
        self.settings.update(settings)
        self.roster = [] # populate via update_cards method
        self.presents = []
        self.device_presents = []
        self.pending_trades = []
        self.woh = WoH(self)

    def get_farm_url(self):
        if self.settings["farm_mission"]:
            return self.woh.URLS[self.settings["farm_mission"]]
        else:
            return False

    def get_card_count(self):
        html = self.woh.parse_page(self.woh.URLS['mypage'])
        if html:
            card_text = html.select(".card a")[0].get_text().strip()
            return int(re.match(r"\d+", card_text).group())
        else:
            return 0

    def update_roster(self):
        new_roster = []
        card_list_urls = [self.woh.URLS['card_list_index'] + str(page) for page in range(0, self.get_card_count(), 10)]
        print "Getting " + str(self.get_card_count()) + " cards..."
        for url in card_list_urls:
            print "Walking " + url + "..."
            html = self.woh.parse_page(url)
            if html:
                #page_cards = html.select("a[href^=" + self.woh.URLS['card_list_desc'] + "]")
                page_cards = html.select("a[href^=" + self.woh.URLS['card_list_desc'] + "] img")
                #page_cards = html.select(".member_bg>div+table~table")

                for card in page_cards:
                    level = ""

                    image_id = re.search(r"\/card\/\w+\/([a-f0-9]+)\.jpg", card.get("src").strip()).group(1)
                    unique_id = re.search(r"desc/(\d+)", card.find_parent("a").get("href")).group(1)
                    if image_id and unique_id:
                        #print "Identifying " + unique_id + " with " + image_id

                        global_properties = self.woh.parse_card_json(image_id)
                        # print global_properties

                        middle_element = card.find_parent("table")
                        #print(middle_element.encode('utf-8'))
                        lvl_element = middle_element.find(name="span", text=re.compile(r"Lv:"))
                        if lvl_element:
                            level_data = lvl_element.find_next_sibling(text=re.compile(r"(\d+)\/\d+"))

                            level =  int(re.search(r"(\d+)\/\d+", level_data.strip()).group(1))

                        properties = {
                            "rarity": global_properties["rarity"],
                            "alignment": global_properties["alignment"],
                            "img_id": image_id,
                            "level": level,
                            "global_id": global_properties["global_id"],
                            "name": global_properties["name"],

                        }

                        #print str(properties).encode('utf-8')
                        #curr_card =

                        #print curr_card.get_unique_id()
                        print "about to append " + global_properties["name"]
                        card_to_append = copy.deepcopy(Card(unique_id, properties))

                        new_roster.append(card_to_append)
                        print "2nd-to-last-card = " + new_roster[len(new_roster)-2].get_name()

        #new_roster = list(set(new_roster))

        for each_card in new_roster:
            print each_card.get_name()

        return

    def delete_cards(self, *card_unique_ids):
        # remove card from catalog by unique_id
        return

    def get_match_for_fuse(self):

        return

    def get_all_cards(self):
        card_urls = ["http://ultimate-a.cygames.jp/ultimate/archive/view_other/00000001/"+str(page)+"/0/1/0/0/0" for page in range(0, self.get_card_count(), 10)]

        return

    def get_sid(self):
        return self.settings["sid"]

    def set_farm_mission(self, farm_mission):
        self.farm_mission = farm_mission

    def get_farm_mission(self):
        return self.farm_mission

    def get_card_space_remaining(self):
        html = self.woh.parse_page(self.woh.URLS['mypage'])
        if html:
            card_text = html.select(".card a")[0].get_text().strip()
            return int(re.search(r"/(\d+)", card_text).group(1)) - int(re.match(r"\d+", card_text).group())

    def get_remaining_energy(self):
        html = self.woh.parse_page(self.woh.URLS['mypage'])
        if html:
            energy_text = html.select(".EnergyPowerTxt")[0].get_text()
            return int(re.match(r"\d+", energy_text).group())
        else:
            return False

    def get_remaining_silver(self):
        html = self.woh.parse_page(self.woh.URLS['mypage'])
        if html:
            return int(html.select(".silver")[0].get_text().strip().replace(',', ''))
        else:
            return False

    def get_remaining_atk_power(self):
        html = self.woh.parse_page(self.woh.URLS['mypage'])
        if html:
            atk_text = html.select(".AttackPowerTxt")[0].get_text()
            return int(re.match(r"\d+", atk_text).group())
        else:
            return False

    def getRallyPoints(self):
        html = self.woh.parse_page(self.woh.URLS['mypage'])
        if html:
            rally_text = html.select(".point")[0].get_text().strip()
            return int(rally_text)
        else:
            return False