import re
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

    def farm_mission(self, operation, mission):
        if operation == 0 or mission == 0:
            operation, mission = self.player.get_newest_mission()

        if mission == "boss":
            self.woh.parse_page(self.woh.get_mission_url(operation, mission))
            print "Farmed Boss at %d-%s" % (operation, mission)
            return True
        else:
            if self.player.get_remaining_energy() >= self.woh.OPERATION_ENERGY_COST[operation]:
                self.woh.parse_page(self.woh.get_mission_url(operation, mission))
                print "Farmed Mission %d-%d" % (operation, mission)
                return True
            else:
                return False


    """
    This function fuses a filtered series of base_cards with a matching fuser_card.
    # fuse_alignment correlates to database alignments. 0 is any, 1 is speed, 2 is bruiser, 3 is tactics
    """
    def smart_fuse(self, fuse_rarity=1, fuse_alignment=0, max_fuse_level=0):
        fused_cards = []
        spent_ids = []

        self.player.update_fusables()
        eligible_fuse_cards = self.player.get_fusables(rarity=fuse_rarity, max_level=max_fuse_level, alignment=fuse_alignment)

        for c in eligible_fuse_cards:
            bgid = c.get_global_id()
            buid = c.get_unique_id()

            if buid not in spent_ids:
                for fc in eligible_fuse_cards:
                    fgid = fc.get_global_id()
                    fuid = fc.get_unique_id()

                    if fgid == bgid and buid != fuid and fuid not in spent_ids:
                        # Fuse base card with fuser
                        fused_card = c.fuse(fuid)
                        if fused_card.get_unique_id() == buid:
                            fused_cards.append(c)
                            spent_ids.append(buid)
                            spent_ids.append(fuid)
                        else:
                            print "Error: Fused result %s does not match expected unique ID %s" % (fused_card.get_unique_id(), buid)

        return fused_cards

    """
    This function boosts a filtered series of base_cards against a filtered series of eligible fuse_cards.
    """
    def smart_boost(self, base_rarity=2, base_version=-1, base_alignment=0, base_max_level=10, base_max_pwr_req=20, boost_rarity=0, boost_count=1, boost_alignment=0, boost_version=0, boost_max_level=1, boost_max_pwr_req=11):
        boosted_cards = []
        spent_ids = []

        # Get all requested cards
        self.player.update_roster()
        base_cards = self.player.get_roster(rarity=base_rarity, version=base_version, alignment=base_alignment, max_level=base_max_level-1, max_pwr_req=base_max_pwr_req)
        boost_cards = self.player.get_roster(rarity=boost_rarity, alignment=boost_alignment, version=boost_version, max_level=boost_max_level, max_pwr_req=boost_max_pwr_req)

        # Sort base cards by fused/unfused
        base_cards.sort(key=lambda c: (c.get_base_rarity(), -c.get_version(), -c.get_level()))
        print "Sorted list..."
        print "..."
        print "Base Cards after sort..."
        for c in base_cards:
            print "r=%d (br=%d + v=%d) @ lvl=%d (%s)" % (c.get_rarity(), c.get_base_rarity(), c.get_version(), c.get_level(), c.get_name())

        # Iterate through each base card
        for curr_card in base_cards:
            card_boosted = False
            base_card = curr_card

            if len(boost_cards) >= 1:
                if base_card.get_unique_id() not in spent_ids:
                    print "Working on " + base_card.get_name() + "/lvl " + str(base_card.get_level())

                    while len(boost_cards) > 0 and base_card.get_level() < base_max_level:
                        # Get set of matching boost cards
                        boost_set = boost_cards[:boost_count]
                        boost_ids = [bcard.get_unique_id() for bcard in boost_set]

                        #print "Found " + str(len(boost_ids)) + " qualifying boosters"
                        print base_card.get_name() + " eligible for boost at lvl " + str(base_card.get_level())
                        result = base_card.boost(boost_ids)

                        if result.get_unique_id() == base_card.get_unique_id():
                            print result.get_name() + " boosted to lvl " + str(result.get_level())
                            base_card = result
                            card_boosted = True

                            # Mark used cards as spent
                            [spent_ids.append(uid) for uid in boost_ids]

                            # Remove used set of boost cards from list
                            boost_cards = boost_cards[boost_count:]

                    if card_boosted:
                        boosted_cards.append(result)
            else:
                print "No more qualifying boosters"
                break

        return boosted_cards

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
                rand = "http://ultimate-a.cygames.jp/ultimate/cheer/comment_check"
                cookies = dict(sid=self.player.get_sid())
                user_agent = {'User-agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B)'}
                p = self.player.get_rally_points()
                if p > 9995:
                    print "Rally point limit reached"
                    break
                payload = {'message': 'rally!', 'sort': '1', 'to_viewer_id': x, 'bef_friendship_point': p, 'aft_friendship_point': p, 'is_message': '0', 'is_cheer': '0', 'is_error': '0', 'ret_act': '0', 'message_id': "", 'page': '0', 'offset': '0'}
                r = requests.post(rand, data=payload, cookies=cookies, headers=user_agent)
                if "Your Rally has reached maximum limit" in r.text:
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
            print int(x)
            rand = "http://ultimate-a.cygames.jp/ultimate/cheer/comment_check"
            cookies = dict(sid=self.player.get_sid())
            user_agent = {'User-agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B)'}
            p = self.player.get_rally_points()
            if p > 9988:
                print "Rally point limit reached"
                break
            payload = {'message': 'rally!', 'sort': '1', 'to_viewer_id': x, 'bef_friendship_point': p, 'aft_friendship_point': p, 'is_message': '0', 'is_cheer': '0', 'is_error': '0', 'ret_act': '0', 'message_id': "", 'page': '0', 'offset': '0'}
            r = requests.post(rand, data=payload, cookies=cookies, headers=user_agent)
            if "Your Rally has reached maximum limit" in r.text:
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