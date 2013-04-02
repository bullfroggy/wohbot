import re
from card import Card
from woh import WoH
import time

class Player(object):
    settings = {
        "sid": "",
        "name": "",
        "level": 0,
        "farm_mission": "",
    }

    def __init__(self, settings):
        self.settings.update(settings)
        self.catalog = [] # populate via update_cards method
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
                        middle_element = card.findParent("table")
                        top_element = middle_element.findPreviousSibling("div")
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

    def get_rally_points(self):
        html = self.woh.parse_page(self.woh.URLS['mypage'])
        if html:
            rally_text = html.select(".point")[0].get_text().strip()
            return int(rally_text)
        else:
            return False

    def card_available(self):
        html = self.woh.parse_page(self.woh.URLS['mypage'])
        if html:
            if "Free Card Pack Available!" in str(html):
                return True
            else:
                return False
        else:
            print "cannot parse"
            return False

    def buy_rally_packs(self, cart):
        rallyURL = self.woh.parse_page(self.woh.URLS['buy_rally_pack'])
        if rallyURL:
            for x in range(0, cart - 1):
                self.woh.parse_page(self.woh.URLS['buy_rally_pack'])
        else:
            return False

        return True

    def free_rally_pack(self):
        rallyURL = self.woh.parse_page(self.woh.URLS['draw_free'])
        if rallyURL:
            self.woh.parse_page(self.woh.URLS['draw_free'])
        else:
            return False

        return True

    def rally_all(self):
        f=open('users.txt')
        for x in f:
            if self.get_rally_points() >= 9997:
                print "Rally point limit reached"
                return True
            start = "http://ultimate-a.cygames.jp/ultimate/cheer/index/"
            ID = int(x)
            startU = "http://ultimate-a.cygames.jp/ultimate/profile/show/"
            URL = start + str(ID)
            userURL = startU + str(ID)
            self.woh.URLS['rally_rand'] = URL
            self.woh.URLS['user_page'] = userURL
            userPage = self.woh.parse_page(userURL)
            #time.sleep(1)
            if userPage:
                if "An error has been detected" not in str(userPage):
                    print ID
                    rallyURL = self.woh.parse_page(URL)
                    #time.sleep(1)
                    if "Received 4 Rally Points!" in str(rallyURL):
                        print "Successfully rallied user"
                    else:
                        print "Could not rally user"
                        if "Your Rally has reached maximum limit" in str(rallyURL):
                            print "Maximum rally limit reached"
                            return True
                        if "excessive tapping" in str(userPage):
                            print "Too many taps"
                        if "excessive tapping" in str(rallyURL):
                            print "Too many taps"
            else:
                return False
        return True

