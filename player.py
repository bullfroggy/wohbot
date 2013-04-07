import re
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
        self.catalog = []  # populate via update_cards method
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

    def update_cards(self):
        new_roster = []
        card_list_urls = [self.woh.URLS['card_list_index'] + str(page) for page in range(0, self.get_card_count(), 10)]
        for url in card_list_urls:
            print "Walking " + url + "..."
            html = self.woh.parse_page(url)
            if html:
                page_cards = html.select("a[href^=" + self.woh.URLS['card_list_desc'] + "]")
                #page_cards = html.select(".member_bg>div+table~table")

                for card in page_cards:
                    unique_id = re.search(r"desc/(\d+)", card.get("href")).group(1)
                    if unique_id:
                        print "Identifying " + unique_id
                        middle_element = card.find_parent("table")
                        top_element = middle_element.find_previous_sibling("div")

                        rarity = re.search(r"\(([\s\w]+)\)", top_element.find("p").get_text()).group(1).strip()

                        if "Common" in rarity:
                            rarity = 0
                        elif "Uncommon" in rarity:
                            rarity = 1
                        elif "Rare" in rarity:
                            rarity = 2
                        elif "S Rare" in rarity:
                            rarity = 3
                        elif "SS Rare" in rarity:
                            rarity = 4
                        elif "U Rare" in rarity:
                            rarity = 5
                        elif "Legendary" in rarity:
                            rarity = 6
                        else:
                            rarity = -1


                        alignment = re.search(r"([A-Z]+)", top_element.find("span").get_text()).group(1).strip()

                        if "SPEED" in alignment:
                            alignment = 1
                        elif "BRUISER" in alignment:
                            alignment = 2
                        elif "TACTICS" in alignment:
                            alignment = 3
                        else:
                            alignment = 0

                        img_id = re.search(r"\/card\/\w+\/([a-f0-9]+)\.jpg", middle_element.find("img").get("src").strip()).group(1)
                        level =  int(re.search(r"Lv:\s+(\d+)\/\d+", middle_element.get_text().strip()).group(1))

                        properties = {
                            "rarity": rarity,
                            "alignment": alignment,
                            "img_id": img_id,
                            "level": level,

                        }

                        print properties
                        #curr_card =

                        #print curr_card.get_unique_id()

                        new_roster.append(Card(unique_id, properties))

        new_roster = list(set(new_roster))

        for each_card in new_roster:
            print each_card.get_img_id()

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

    def get_newest_mission(self):
        html = self.woh.parse_page(self.woh.URLS['mypage'])
        newest_mission_link = html.select("#newestMission a")[0].get('href')
        if "boss" in newest_mission_link:
            html = self.woh.parse_page(self.woh.URLS['quest_index'])
            operation_text = html.select(".window3")[0].get_text()
            operation = int(re.search(r"Operation\s(\d+):", operation_text).group(1))
            mission = "boss"
        else:
            operation = int(re.search(r"(\d+)/(\d+)", newest_mission_link).group(1))
            mission = int(re.search(r"(\d+)/(\d+)", newest_mission_link).group(2))
        return operation, mission

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