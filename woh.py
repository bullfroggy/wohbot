import requests
from bs4 import BeautifulSoup


class WoH(object):
    URLS = {
        "mypage": "http://ultimate-a.cygames.jp/ultimate/mypage/index",
        "fusion": "http://ultimate-a.cygames.jp/ultimate/card_union",
        "quest_index": "http://ultimate-a.cygames.jp/ultimate/quest",
        "mission_23": "http://ultimate-a.cygames.jp/ultimate/quest/play/2/3",
        "mission_24": "http://ultimate-a.cygames.jp/ultimate/quest/play/2/4",
        "card_list_index": "http://ultimate-a.cygames.jp/ultimate/card_list/index/%d/1/0/%d",
        "card_list_desc": "http://ultimate-a.cygames.jp/ultimate/card_list/desc/",
        "fuse_eligible_list": "http://ultimate-a.cygames.jp/ultimate/card_union/union_card/%d/1/0/%d",
        "fuse_base_set": "http://ultimate-a.cygames.jp/ultimate/card_union/union_change/",
        "fuse_card_set": "http://ultimate-a.cygames.jp/ultimate/card_union/synthesis/%s?sleeve_str=%s",
        "boost_base_set": "http://ultimate-a.cygames.jp/ultimate/card_str/base_change/",
        "boost_card_set": "http://ultimate-a.cygames.jp/ultimate/card_str/strengthen/",
        "boost_result": "http://ultimate-a.cygames.jp/ultimate/card_str/index/-1/0",
        "present_list": "http://ultimate-a.cygames.jp/ultimate/present/recieve/0/0/?view_auth_type=1",
        "present_reg_list": "http://ultimate-a.cygames.jp/ultimate/present/recieve/1/0/?view_auth_type=2",
        "present_claim": "http://ultimate-a.cygames.jp/ultimate/present/recieve",
        "card_api": "http://rpgotg.herokuapp.com/api/v1/cards/",
    }
    OPERATION_ENERGY_COST = {
        1: 1,
        2: 1,
        3: 2,
        4: 3,
        5: 4,
        6: 5,
        7: 6,
        8: 7,
        9: 8,
        10: 9,
        11: 10,
        12: 11,
        13: 12,
        14: 10,
        15: 11,
        16: 12,
        17: 13,
        18: 10,
        19: 11,
        20: 12,
        21: 13,
    }


    def __init__(self, player):
        self.player = player

    def get_url(self, url):
        if self.URLS[url]:
            return self.URLS[url]
        else:
            return False

    def get_mission_url(self, operation, mission):
        if mission == "boss":
            self.parse_page("http://ultimate-a.cygames.jp/ultimate/quest_boss/appear/%d" % operation, req="post")
            self.parse_page("http://ultimate-a.cygames.jp/ultimate/smart_phone_flash/quest_boss/%d" % operation, req="post")
            self.parse_page("http://ultimate-a.cygames.jp/ultimate/quest_boss/boss_play_swf/%d" % operation)
            return "http://ultimate-a.cygames.jp/ultimate/quest_boss/result/%d/1/0" % operation
        else:
            return "http://ultimate-a.cygames.jp/ultimate/quest/play/%d/%d" % (operation, mission)

    def parse_page(self, url, req="get", payload=dict("")):

        cookies = dict(sid=self.player.get_sid())
        user_agent = {"User-Agent": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19"}

        if req=="get":
            r = requests.get(url, headers=user_agent, cookies=cookies, data=payload)
        elif req=="post":
            r = requests.post(url, headers=user_agent, cookies=cookies, data=payload)

        if r:
            return BeautifulSoup(r.text)
        else:
            return False

    def log_card_stats(self, global_id, card_atk, card_def):
        if (global_id and card_atk and card_def):
            # send a req to log form with data
            payload = {
                "max_attack": card_atk, 
                "max_defense": card_def,
            }
            print "Logging %s into card %d" % (repr(payload), global_id)
        return requests.put(self.URLS["card_api"] + "%d/" % global_id, data=payload)

    def parse_json(self, url, req="get", payload=dict("")):
        if req=="get":
            r = requests.get(url, data=payload)
        elif req=="post":
            r = requests.post(url, data=payload)
        
        if r:
            return r.json()
        else:
            return False

    def parse_card_json(self, card_id):
        return self.parse_json(self.get_url("card_api") + card_id)

