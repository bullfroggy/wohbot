import re
from woh import WoH


class Bot(object):
    settings = {
        "player": None,
    }
    player = None

    def __init__(self, settings):
        self.settings.update(settings)
        self.player = self.settings["player"]
        self.woh = WoH(self.player)


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

        # fuse_alignment correlates to database alignments. 0 is any, 1 is speed, 2 is bruiser, 3 is tactics
    def smart_fuse(self, fuse_rarity=1, fuse_alignment=0, max_fuse_level=0):
        self.player.update_roster()

        p_roster = self.player.get_roster()
        print len(p_roster)

        fuse_card_list_url = str(self.woh.URLS['fuse_eligible_list']) % (fuse_alignment, 0)
        eligible_fuse_cards = []

        #print "Fetching " + fuse_card_list_url + "..."
        index = self.woh.parse_page(fuse_card_list_url)
        if index:
            # TO DO: Need to get the last page better
            fuse_pages = int(re.search(r"union_card\/\d+\/\d+\/\d+\/(\d+)", index.select(".flickSimple a.a_link")[-1].get("href").strip()).group(1))
            print "Parsing %d fuse pages..." % fuse_pages
            r_fuse_list_urls = [str(self.woh.URLS['fuse_eligible_list']) % (0, page) for page in range(0, fuse_pages+1, 10)]

            for url in r_fuse_list_urls:
                print "Walking " + url + "..."
                html = self.woh.parse_page(url)
                if html:
                    page_cards = html.select("a[href^=" + self.woh.URLS['fuse_base_set'] + "]")

                    for card in page_cards:
                        unique_id = re.search(r"union_change/(\d+)", card.get("href")).group(1)
                        curr_card = self.player.get_card(unique_id)
                        
                        if (curr_card not in eligible_fuse_cards and
                            (fuse_rarity == 0 or curr_card.get_rarity() == fuse_rarity) and
                            (fuse_alignment == 0 or curr_card.get_alignment() == fuse_alignment) and
                            (max_fuse_level == 0 or curr_card.get_level() <= max_fuse_level)):
                            eligible_fuse_cards.append(curr_card)
        fused_cards = []

        for c in eligible_fuse_cards:
            #if c.get_global_id() 
            print "I'd fuse this card: " + c.get_name()
            #fuse_cards.append(c.fuse())


        #self.player.update_roster()

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

                    self.player.update_roster()

        return base_card
