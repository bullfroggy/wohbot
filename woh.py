import requests
from bs4 import BeautifulSoup


class WoH(object):
    URLS = {
        "mypage": "http://ultimate-a.cygames.jp/ultimate/mypage/index",
        "fusion": "http://ultimate-a.cygames.jp/ultimate/card_union",
        "mission_23": "http://ultimate-a.cygames.jp/ultimate/quest/play/2/3",
        "mission_24": "http://ultimate-a.cygames.jp/ultimate/quest/play/2/4",
        "card_list_index": "http://ultimate-a.cygames.jp/ultimate/card_list/index/0/1/0/",
        "card_list_desc": "http://ultimate-a.cygames.jp/ultimate/card_list/desc/",
        "packs": "http://ultimate-a.cygames.jp/ultimate/gacha/index/0",
	    "draw_free": "http://ultimate-a.cygames.jp/ultimate/gacha/draw_free",
        "buy_rally_pack": "http://ultimate-a.cygames.jp/ultimate/gacha/draw_free/1",
        "friend_list": "http://ultimate-a.cygames.jp/ultimate/friend?p=",
        "fuse_eligible_list": "http://ultimate-a.cygames.jp/ultimate/card_union/union_card/%s/1/0/",
        "fuse_base_set": "http://ultimate-a.cygames.jp/ultimate/card_union/union_change/",
        "fuse_card_set": "http://ultimate-a.cygames.jp/ultimate/card_union/synthesis/",
        "quest_index": "http://ultimate-a.cygames.jp/ultimate/quest"
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
        user_agent = {'User-agent': 'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B)'}
        cookies = dict(sid=self.player.get_sid())
        #print "getting " + url + " with SID " + self.player.get_sid()
        if req=="get":
            r = requests.get(url, cookies=cookies, data=payload)
        elif req=="post":
            r = requests.post(url, cookies=cookies, data=payload, headers=user_agent)

        if r.status_code == 200:
            return BeautifulSoup(r.text)
        else:
            return False