from woh import WoH
import requests


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

    def max_farm(self):
        required_battles = int(self.player.get_remaining_energy() / 3)
        self.farm(required_battles)

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

    def message_friends(self):
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
                        user_agent = {'User-agent': 'Mozilla/5.0'}
                        payload = {'message': 'rally!', 'sort': '1', 'to_viewer_id': x, 'bef_friendship_point': p, 'aft_friendship_point': p, 'is_message': '0', 'is_cheer': '0', 'is_error': '0', 'ret_act': '0', 'message_id': mess, 'page': '0', 'offset': '0'}
                        r = requests.post(rand, data=payload, cookies=cookies, headers=user_agent)
                        moreLines = r.text.splitlines()
                        for line in moreLines:
                            if "ultimate/cheer/send_check" in line:
                                rand = line.split("'")[1]
                                cookies = dict(sid=self.player.get_sid())
                                user_agent = {'User-agent': 'Mozilla/5.0'}
                                payload = {'to_viewer_id': x, 'ret_act': '0', 'message_id': "", 'sort': '1', 'page': '0'}
                                requests.post(rand, data=payload, cookies=cookies, headers=user_agent)
                                print "Sending message"
        return True

    def message_randoms(self):
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
                                user_agent = {'User-agent': 'Mozilla/5.0'}
                                payload = {'message': 'rally!', 'sort': '1', 'to_viewer_id': x, 'bef_friendship_point': p, 'aft_friendship_point': p, 'is_message': '0', 'is_cheer': '0', 'is_error': '0', 'ret_act': '0', 'message_id': mess, 'page': '0', 'offset': '0'}
                                r = requests.post(rand, data=payload, cookies=cookies, headers=user_agent)
                                moreLines = r.text.splitlines()
                                for line in moreLines:
                                    if "ultimate/cheer/send_check" in line:
                                        rand = line.split("'")[1]
                                        cookies = dict(sid=self.player.get_sid())
                                        user_agent = {'User-agent': 'Mozilla/5.0'}
                                        payload = {'to_viewer_id': x, 'ret_act': '0', 'message_id': "", 'sort': '1', 'page': '0'}
                                        requests.post(rand, data=payload, cookies=cookies, headers=user_agent)
                                        print "Sending message"
                                        count += 1
                else:
                    break
            else:
                break
        return True