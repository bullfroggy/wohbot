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
        "packs": "http://ultimate-a.cygames.jp/ultimate/gacha?viewer_id=null",
        "get_free_pack": "http://ultimate-a.cygames.jp/ultimate/gacha/show_swf/?payment_id=-1364576248-4289&rnd=404849116&viewer_id=null",
        "get_free_pack1": "http://ultimate-a.cygames.jp/ultimate/gacha/draw_free?rnd=859046128",
        "buy_rally_pack": "http://ultimate-a.cygames.jp/ultimate/smart_phone_flash/convertGacha/3600000/gachaSsSsdo_swfSsSs?t=1&c%5B0%5D=2110040&s%5B0%5D=10471578212&f%5B0%5D=0&fid=0900_free_gacha.swf&effect=0&ticket_type=0&ticket_id=0&ticket_cost=0&rnd=641405065&viewer_id=null"
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