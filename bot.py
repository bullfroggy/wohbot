from woh import WoH
import requests
import time


class Bot(object):
    settings = {
        "player": None,
    }
    player = None

    def __init__(self, settings):
        self.settings.update(settings)
        self.player = self.settings["player"]
        self.woh = WoH(self.player)

    def update_roster(self):
        return self.player.update_cards()

    def farm(self, iterations):
        mission_url = self.player.get_farm_url()

        print "Running the farm %s times." % iterations
        if self.woh.parse_page(mission_url):
            for x in range(0, iterations - 1):
                self.woh.parse_page(mission_url)
        else:
            return False

        return True

    def farm_mission(self, mission_url):
        self.woh.parse_page(mission_url)
        return True

    def farm_newest_mission(self):
        operation, mission = self.player.get_newest_mission()
        # Only Farm the Mission if you have enough energy for at least one attack
        if mission != "boss":
            if self.player.get_remaining_energy() >= self.woh.OPERATION_ENERGY_COST[operation]:
                self.farm_mission(self.woh.get_mission_url(operation, mission))
                return True
            else:
                return False
        else:
            self.farm_mission(self.woh.get_mission_url(operation, mission))
            return True

    def max_farm_newest_mission(self):
        while self.farm_newest_mission():
            print "Farmed"

    def max_farm(self, operation, mission):
        required_battles = int(self.player.get_remaining_energy() / 3)
        for x in range(0, required_battles):
            self.farm_mission(self.woh.get_mission_url(operation, mission))

        # fuse_alignment correlates to database alignments. 0 is any, 1 is speed, 2 is bruiser, 3 is tactics
    def smart_fuse(self, fuse_rarity=1, fuse_alignment=0, max_fuse_level=0):
        fuse_card_list_url = str(self.woh.URLS['fuse_eligible_list']).replace("%s", str(fuse_alignment))
        eligible_fuse_cards = []
        print "Fetching " + fuse_card_list_url + "..."
        index = self.woh.parse_page(fuse_card_list_url)
        if index:
            # TO DO: Need to get the last page better
            fuse_pages = int(len(index.select(".flickSimple a.a_link")))
            print "Parsing " + str(fuse_pages) + " fuse pages..."
            r_fuse_list_urls = [self.woh.URLS['fuse_eligible_list'] + str(page) for page in range(0, fuse_pages, 10)]

            for url in r_fuse_list_urls:
                print "Walking " + url + "..."
                html = self.woh.parse_page(url)
                if html:
                    page_cards = html.select("a[href^=" + self.woh.URLS['fuse_base_set'] + "]")

                    for card in page_cards:
                        unique_id = re.search(r"desc/(\d+)", card.get("href")).group(1)
                        if unique_id:
                            middle_element = card.find_parent("table")
                            top_element = middle_element.find_previous_sibling("div")
                            #print top_element
                            rarity = re.search(r"\((\w+)\)", top_element.find("p")).group(1).strip()
                            print "Rarity: " + rarity
                            alignment = re.search(r"(\W+)", str(top_element.find("span"))).group(1).strip()

                            properties = {
                                "rarity": rarity,
                                "alignment": alignment,

                            }
                            #curr_card =

                            #print curr_card.get_unique_id()

                            eligible_fuse_cards.append(Card(unique_id, properties))

        eligible_fuse_cards = list(set(eligible_fuse_cards))

        for each_card in eligible_fuse_cards:
            print each_card.get_alignment()

            if fuse_base.get_rarity() == fuse_rarity:
                if fuse_alignment == 0 or fuse_base.get_alignment() == fuse_alignment:
                    r_fuse_base = self.woh.parse_page(self.woh.URLS["fuse_base_set"] + fuse_base.get_unique_id())
                    if r_fuse_base:
                        # read HTML to confirm base is right
                        pass

        self.player.update_cards()

        return

    def smart_boost(self, base_card, boost_rarity=0, boost_count=10):
        set_base_card_url = "http://ultimate-a.cygames.jp/ultimate/card_str/base_change/" + base_card.get_unique_id()

        eligible_cards = []

        for boost_card in self.card_catalog:
            if boost_card.get_rarity() == boost_rarity:
                if len(eligible_cards) < boost_count:
                    eligible_cards.append(boost_card)

        if len(eligible_cards) > 0:
            r_set_base = self.woh.parse_page(set_base_card_url)
            if r_set_base:
                # read the HTML to confirm base is right

                unique_id_url_str = "_".join(eligible_cards)
                boost_confirm_url = "http://ultimate-a.cygames.jp/ultimate/app_manage/post_redirection/?url=card_str%2Fstrengthen%2F" + unique_id_url_str
                post_data = {'sleevestr': unique_id_url_str}

                r_boost_confirm = self.woh.parse_page(boost_confirm_url, req="post", payload=post_data)
                if r_boost_confirm:
                    # read HTML to confirm base is right

                    #success!

                    self.update_cards()

        return base_card

    def buy_rally_packs(self, cart):
        rallyURL = self.woh.parse_page(self.woh.URLS['buy_rally_pack'])
        if rallyURL:
            for x in range(0, cart - 1):
                self.woh.parse_page(self.woh.URLS['buy_rally_pack'])
        else:
            return False
        return True

    def get_free_pack(self):
        rallyURL = self.woh.parse_page(self.woh.URLS['draw_free'])
        if rallyURL:
            self.woh.parse_page(self.woh.URLS['draw_free'])
        else:
            return False
        return True

    def rally_randoms(self):
        f = open('users.txt')
        for x in f:
            if self.player.get_rally_points() >= 9995:
                print "Rally point limit reached"
                return True
            start = "http://ultimate-a.cygames.jp/ultimate/cheer/index/"
            ID = int(x)
            URL = start + str(ID)
            #time.sleep(1)
            print ID
            rallyURL = self.woh.parse_page(URL)
            #time.sleep(1)
            if "You rallied" in str(rallyURL):
                print "Successfully rallied user"
            else:
                print "Could not rally user"
                if "Your Rally has reached maximum limit" in str(rallyURL):
                    print "Maximum rally limit reached"
                    return True
                if "excessive tapping" in str(rallyURL):
                    print "Too many taps"
        return True

    def rally_friends(self):
        f = self.player.get_friend_list()
        for x in f:
            if self.player.get_rally_points() >= 9993:
                print "Rally point limit reached"
                return True
            start = "http://ultimate-a.cygames.jp/ultimate/cheer/index/"
            ID = int(x)
            URL = start + str(ID)
            #time.sleep(1)
            print ID
            rallyURL = self.woh.parse_page(URL)
            #time.sleep(1)
            if "You rallied" in str(rallyURL):
                print "Successfully rallied user"
            else:
                print "Could not rally user"
                if "Your Rally has reached maximum limit" in str(rallyURL):
                    print "Maximum rally limit reached"
                    return True
                if "excessive tapping" in str(rallyURL):
                    print "Too many taps"
        return True

    def remove_message(self, x):
        start = "http://ultimate-a.cygames.jp/ultimate/profile/show/"
        URL = start + str(x)
        userURL = self.woh.parse_page(URL)
        URLines = str(userURL).splitlines()
        for line in URLines:
            if "ultimate/cheer/remove_comment" in line:
                deleteURL = line.split('"')[3]
                r = self.woh.parse_page(deleteURL)
                Deleter = str(r).splitlines()
                for line in Deleter:
                    if "message_id" in line:
                        message_id = line.split('"')[5]
                    if "viewer_id" in line:
                        viewer_id = line.split('"')[5]
                    if "friend_id" in line:
                        friend_id = line.split('"')[5]
                for line in Deleter:
                    if "ultimate/cheer/exec_remove" in line:
                        deleteNOW = line.split('"')[1]
                        cookies = dict(sid=self.player.get_sid())
                        user_agent = {'User-agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B)'}
                        payload = {'message_id': message_id, 'viewer_id': viewer_id, 'friend_id': friend_id}
                        a = requests.post(deleteNOW, data=payload, cookies=cookies, headers=user_agent)
                        if "You have deleted a Rally." in a.text:
                            print "Message Deleted"
                break

    def message_randoms(self):
        f = open('users.txt')
        random_num = self.player.get_num_randoms()
        count = 0
        for x in f:
            print int(x)
            if random_num > count:
                p = self.player.get_rally_points()
                rand = "http://ultimate-a.cygames.jp/ultimate/cheer/comment_check"
                cookies = dict(sid=self.player.get_sid())
                user_agent = {'User-agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B)'}
                payload = {'message': 'rally!', 'sort': '1', 'to_viewer_id': x, 'bef_friendship_point': p, 'aft_friendship_point': p, 'is_message': '0', 'is_cheer': '0', 'is_error': '0', 'ret_act': '0', 'message_id': "", 'page': '0', 'offset': '0'}
                r = requests.post(rand, data=payload, cookies=cookies, headers=user_agent)
                p = self.player.get_rally_points()
                if "Your Rally has reached maximum limit" in r.text:
                    break
                if p > 9988:
                    break
                moreLines = r.text.splitlines()
                for line in moreLines:
                    if "ultimate/cheer/send_check" in line:
                        rand = line.split("'")[1]
                        cookies = dict(sid=self.player.get_sid())
                        user_agent = {'User-agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B)'}
                        payload = {'to_viewer_id': x, 'ret_act': '0', 'message_id': "", 'sort': '1', 'page': '0'}
                        requests.post(rand, data=payload, cookies=cookies, headers=user_agent)
                        count += 1
                        print "Sending message"
                        self.remove_message(int(x))
            else:
                break
        return True

    def message_friends(self):
        f = self.player.get_friend_list()
        for x in f:
            rand = "http://ultimate-a.cygames.jp/ultimate/cheer/comment_check"
            cookies = dict(sid=self.player.get_sid())
            user_agent = {'User-agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B)'}
            payload = {'message': 'rally!', 'sort': '1', 'to_viewer_id': x, 'bef_friendship_point': p, 'aft_friendship_point': p, 'is_message': '0', 'is_cheer': '0', 'is_error': '0', 'ret_act': '0', 'message_id': "", 'page': '0', 'offset': '0'}
            r = requests.post(rand, data=payload, cookies=cookies, headers=user_agent)
            p = self.player.get_rally_points()
            if "Your Rally has reached maximum limit" in r.text:
                break
            if p > 9988:
                break
            moreLines = r.text.splitlines()
            for line in moreLines:
                if "ultimate/cheer/send_check" in line:
                    rand = line.split("'")[1]
                    cookies = dict(sid=self.player.get_sid())
                    user_agent = {'User-agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B)'}
                    payload = {'to_viewer_id': x, 'ret_act': '0', 'message_id': "", 'sort': '1', 'page': '0'}
                    requests.post(rand, data=payload, cookies=cookies, headers=user_agent)
                    print "Sending message"
                    self.remove_message(int(x))
        return True

    def rally_message_friends(self):

        f = self.player.get_friend_list()
        for x in f:
            p = self.player.get_rally_points()
            print p, "rally points"
            if p >= 9981:
                print "Rally point limit reached"
                return True
            start = "http://ultimate-a.cygames.jp/ultimate/cheer/index/"
            ID = int(x)
            URL = start + str(ID)
            #time.sleep(1)
            print "Rallying user", ID
            rallyURL = self.woh.parse_page(URL)
            #time.sleep(1)
            while "but did not receive any Rally Points" in str(rallyURL):
                time.sleep(10)
                rallyURL = self.woh.parse_page(URL)
            if "You rallied" in str(rallyURL):
                print "Successfully rallied user"
            else:
                print "Could not rally user"
                if "Your Rally has reached maximum limit" in str(rallyURL):
                    print "Maximum rally limit reached"
                    return True
                if "excessive tapping" in str(rallyURL):
                    print "Too many taps"
            if "12 Rally Points by sending a message!" in str(rallyURL):
                lines = str(rallyURL).splitlines()
                mess = ""
                for line in lines:
                    if 'name="message_id"' in line:
                        mess = line.split('"')[5]
                    if "ultimate/cheer/comment_check" in line:
                        p = self.player.get_rally_points()
                        rand = line.split('"')[1]
                        cookies = dict(sid=self.player.get_sid())
                        user_agent = {'User-agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B)'}
                        payload = {'message': 'rally!', 'sort': '1', 'to_viewer_id': x, 'bef_friendship_point': p, 'aft_friendship_point': p, 'is_message': '0', 'is_cheer': '0', 'is_error': '0', 'ret_act': '0', 'message_id': mess, 'page': '0', 'offset': '0'}
                        r = requests.post(rand, data=payload, cookies=cookies, headers=user_agent)
                        moreLines = r.text.splitlines()
                        for line in moreLines:
                            if "ultimate/cheer/send_check" in line:
                                rand = line.split("'")[1]
                                cookies = dict(sid=self.player.get_sid())
                                user_agent = {'User-agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B)'}
                                payload = {'to_viewer_id': x, 'ret_act': '0', 'message_id': "", 'sort': '1', 'page': '0'}
                                requests.post(rand, data=payload, cookies=cookies, headers=user_agent)
                                print "Sending message"
                                self.remove_message(int(x))
        return True

    def rally_message_randoms(self):
        friends = self.player.get_friend_list()
        f = open('users.txt')
        random_num = self.player.get_num_randoms()
        count = 0
        for x in f:
            if random_num > count:
                p = self.player.get_rally_points()
                print p, "rally points"
                if p >= 9991:
                    print "Rally point limit reached"
                    return True
                start = "http://ultimate-a.cygames.jp/ultimate/cheer/index/"
                ID = int(x)
                URL = start + str(ID)
                #time.sleep(1)
                if x in friends:
                    continue
                print "Rallying user", ID
                rallyURL = self.woh.parse_page(URL)
                #time.sleep(1)
                if "You rallied" in str(rallyURL):
                    print "Successfully rallied user"
                    count += 1
                else:
                    print "Could not rally user"
                    if "Your Rally has reached maximum limit" in str(rallyURL):
                        print "Maximum rally limit reached"
                        return True
                    if "excessive tapping" in str(rallyURL):
                        print "Too many taps"
                if random_num > count:
                    if "6 Rally Points by sending a message!" in str(rallyURL):
                        lines = str(rallyURL).splitlines()
                        mess = ""
                        for line in lines:
                            if 'name="message_id"' in line:
                                mess = line.split('"')[5]
                            if "ultimate/cheer/comment_check" in line:
                                p = self.player.get_rally_points()
                                rand = line.split('"')[1]
                                cookies = dict(sid=self.player.get_sid())
                                user_agent = {'User-agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B)'}
                                payload = {'message': 'rally!', 'sort': '1', 'to_viewer_id': x, 'bef_friendship_point': p, 'aft_friendship_point': p, 'is_message': '0', 'is_cheer': '0', 'is_error': '0', 'ret_act': '0', 'message_id': mess, 'page': '0', 'offset': '0'}
                                r = requests.post(rand, data=payload, cookies=cookies, headers=user_agent)
                                moreLines = r.text.splitlines()
                                for line in moreLines:
                                    if "ultimate/cheer/send_check" in line:
                                        rand = line.split("'")[1]
                                        cookies = dict(sid=self.player.get_sid())
                                        user_agent = {'User-agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B)'}
                                        payload = {'to_viewer_id': x, 'ret_act': '0', 'message_id': "", 'sort': '1', 'page': '0'}
                                        requests.post(rand, data=payload, cookies=cookies, headers=user_agent)
                                        print "Sending message"
                                        count += 1
                                        self.remove_message(int(x))
                else:
                    break
            else:
                break
        return True