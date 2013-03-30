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
        "buy_rally_pack": "http://ultimate-a.cygames.jp/ultimate/gacha/draw_free/1"
    }

    def __init__(self, player):
        self.player = player

    def get_url(self, url):
        if self.URLS[url]:
            return self.URLS[url]
        else:
            return False

    def parse_page(self, url):
        cookies = dict(sid=self.player.get_sid())
        r = requests.get(url, cookies=cookies)
        if r.status_code == 200:
            return BeautifulSoup(r.text)
        else:
            return False