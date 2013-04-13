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
        self.roster = [] # populate via update_roster()
        self.fusables = [] # populate via update_fusables()
        self.presents = []
        self.device_presents = []
        self.pending_trades = []
        self.woh = WoH(self)

    def get_farm_url(self):
        if self.settings["farm_mission"]:
            return self.woh.URLS[self.settings["farm_mission"]]
        else:
            return False

    def get_card_count(self, alignment=0):
        html = self.woh.parse_page(self.woh.URLS['mypage'])
        if html:
            card_text = html.select(".card a")[0].get_text().strip()
            return int(re.match(r"\d+", card_text).group())
        else:
            return 0
        """
        # Trying to make an alignment-specific card_count
        url = str(self.woh.URLS['card_list_index']) % (int(alignment), 0)
        print "get_card_count " + url
        html = self.woh.parse_page(url)
        if html.select(".flickSimple a.a_link"):
            last_page_url = html.select(".flickSimple a.a_link")[-1].get("href")
            last_page_marker = re.search(r"index\/\d+\/\d+\/\d+\/(\d+)", last_page_url)
            if last_page_marker:
                card_count = int(last_page_marker.group(1))
            else:
                card_count = 0
            print card_count
            
            max_card_url = str(self.woh.URLS['card_list_index']) % (int(alignment), card_count)
            print max_card_url
            card_html = self.woh.parse_page(max_card_url)
            
            last_page_card_count = card_html.select("a[href^=\'/desc/\'] img")
            print len(last_page_card_count)
            if last_page_card_count:
                card_count += len(last_page_card_count)

            print card_count

            return card_count
        else:
            return 0
        """

    def update_fusables(self):
        fuse_card_list_url = str(self.woh.URLS['fuse_eligible_list']) % (0, 0)
        eligible_fuse_cards = []

        index = self.woh.parse_page(fuse_card_list_url)
        if index:
            if not index.select(".flickSimple a.a_link"):
                # There is just one page of cards
                fuse_pages = 10
            else:
                # TO DO: Need to get the last page better
                fuse_pages = int(re.search(r"union_card\/\d+\/\d+\/\d+\/(\d+)", index.select(".flickSimple a.a_link")[-1].get("href").strip()).group(1))

            print "Getting fusables (up to marker %d)..." % fuse_pages
            r_fuse_list_urls = [str(self.woh.URLS['fuse_eligible_list']) % (0, page) for page in range(0, fuse_pages+1, 10)]

            for url in r_fuse_list_urls:
                print "Walking " + url + "..."
                html = self.woh.parse_page(url)
                if html:
                    page_cards = html.select("a[href^=" + self.woh.URLS['fuse_base_set'] + "]")

                    for card in page_cards:
                        curr_card = None

                        thumbnail = card.find_parent("div").find_parent("div").find("img")
                        if thumbnail:
                            image_id = re.search(r"\/card\/\w+\/([a-f0-9]+)\.jpg", thumbnail.get("src").strip()).group(1)

                        unique_id = re.search(r"union_change/(\d+)", card.get("href")).group(1)

                        if image_id and unique_id:

                            global_properties = self.woh.parse_card_json(image_id)
                            middle_element = card.find_parent("table")
                            lvl_element = middle_element.find(name="span", text=re.compile(r"Lv:"))

                            if lvl_element:
                                level_data = lvl_element.find_next_sibling(text=re.compile(r"(\d+)\/\d+"))

                                level =  int(re.search(r"(\d+)\/\d+", level_data.strip()).group(1))


                                properties = {
                                    "global_id": global_properties["global_id"],
                                    "img_id": image_id,
                                    "name": global_properties["name"],
                                    "rarity": global_properties["rarity"],
                                    "alignment": global_properties["alignment"],
                                    "pwr_req": global_properties["power_required"],
                                    "level": level,

                                }
                                #print "found " + unique_id

                                curr_card = Card(self, unique_id, properties)

                        
                        if curr_card not in eligible_fuse_cards:
                            #print "adding " + unique_id + " to eligible list"
                            eligible_fuse_cards.append(curr_card)

        self.fusables = eligible_fuse_cards

        return

    def update_roster(self):
        new_roster = []
        card_list_urls = [self.woh.URLS['card_list_index'] + str(page) for page in range(0, self.get_card_count(alignment=0), 10)]
        print "Updating roster (" + str(self.get_card_count(alignment=0)) + " cards)"
        for url in card_list_urls:
            #print url % (0,0)
            # Walk through each page of cards in roster
            html = self.woh.parse_page(url % (0, 0))
            if html:
                page_cards = html.select("a[href^=" + self.woh.URLS['card_list_desc'] + "] img")
                
                for card in page_cards:

                    level = ""
                    image_id = re.search(r"\/card\/\w+\/([a-f0-9]+)\.jpg", card.get("src").strip()).group(1)
                    unique_id = re.search(r"desc/(\d+)", card.find_parent("a").get("href")).group(1)

                    if image_id and unique_id:

                        global_properties = self.woh.parse_card_json(image_id)

                        middle_element = card.find_parent("table")

                        lvl_element = middle_element.find(name="span", text=re.compile(r"Lv:"))

                        if lvl_element:
                            level_data = lvl_element.find_next_sibling(text=re.compile(r"(\d+)\/\d+"))

                            level =  int(re.search(r"(\d+)\/\d+", level_data.strip()).group(1))

                        properties = {
                            "global_id": global_properties["global_id"],
                            "img_id": image_id,
                            "name": global_properties["name"],
                            "rarity": global_properties["rarity"],
                            "alignment": global_properties["alignment"],
                            "pwr_req": global_properties["power_required"],
                            "level": level,

                        }

                        curr_card = Card(self, unique_id, properties)

                        if curr_card not in new_roster:
                            new_roster.append(curr_card)

        self.roster = new_roster

        return

    def delete_cards(self, *card_unique_ids):
        # remove card from catalog by unique_id
        return

    def get_match_for_fuse(self):

        return

    def get_roster(self, rarity=-1, alignment=0, level=0, max_level=0, max_pwr_req=0, version=-1):
        filtered_roster = []

        for c in self.roster:
            if (rarity == -1 or c.get_rarity() == rarity and
                (alignment == 0 or c.get_alignment() == alignment) and
                (max_level==0 or c.get_level() <= max_level) and
                (max_pwr_req==0 or c.get_pwr_req() <= max_pwr_req) and
                (level == 0 or c.get_level() == level) and
                (version == -1 or c.get_version() == version)):
                filtered_roster.append(c)

        return filtered_roster

    def get_fusables(self, rarity=-1, alignment=0, level=0, max_level=0):
        filtered_cards = []

        for c in self.fusables:
            if (rarity == -1 or c.get_rarity() == rarity and
                (alignment == 0 or c.get_alignment() == alignment) and
                (max_level==0 or c.get_level() <= max_level) and
                (level == 0 or c.get_level() == level)):
                filtered_cards.append(c)

        return filtered_cards

    def get_sid(self):
        return self.settings["sid"]

    def set_farm_mission(self, farm_mission):
        self.farm_mission = farm_mission

    def get_farm_mission(self):
        return self.farm_mission

    def get_card(self, unique_id):
        for c in self.roster:
            if c.get_unique_id() == unique_id:
                print "i found UID " + unique_id
                break
        else:
            c = None

        return c
        
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