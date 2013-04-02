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
        "fuse_eligible_list": "http://ultimate-a.cygames.jp/ultimate/card_union/union_card/%s/1/0/",
        "fuse_base_set": "http://ultimate-a.cygames.jp/ultimate/card_union/union_change/",
        "fuse_card_set": "http://ultimate-a.cygames.jp/ultimate/card_union/synthesis/",
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
        #print "getting " + url + " with SID " + self.player.get_sid()
        if req=="get":
            r = requests.get(url, cookies=cookies, data=payload)
        elif req=="post":
            r = requests.post(url, cookies=cookies, data=payload)

        if r.status_code == 200:
            return BeautifulSoup(r.text)
        else:
            return False