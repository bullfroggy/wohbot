import requests
from bs4 import BeautifulSoup


class WoH(object):
    URLS = {
        "mypage": "http://ultimate-a.cygames.jp/ultimate/mypage/index",
        "fusion": "http://ultimate-a.cygames.jp/ultimate/card_union",
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

    def parse_page(self, url, req="get", payload=dict("")):

        cookies = dict(sid=self.player.get_sid())
        user_agent = {"User-Agent": "Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19"}

        if req=="get":
            r = requests.get(url, headers=user_agent, cookies=cookies, data=payload)
        elif req=="post":
            r = requests.post(url, headers=user_agent, cookies=cookies, data=payload)

        r.raise_for_status()
        return BeautifulSoup(r.text)

    def parse_json(self, url, req="get", payload=dict("")):
        if req=="get":
            r = requests.get(url, data=payload)
        elif req=="post":
            r = requests.post(url, data=payload)
        r.raise_for_status()
        return r.json()

    def parse_card_json(self, card_id):
        return self.parse_json(self.get_url("card_api") + card_id)

