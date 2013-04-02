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

    def smart_fuse(self, base_card, fuser_card):


                self.update_cards()

        return base_card

    def boost(self, base_card, boost_rarity=0, boost_count=10):
        set_base_card_url = "http://ultimate-a.cygames.jp/ultimate/card_str/base_change/" + base_card.get_unique_id()

        eligible_cards = []

        for boost_card in card_catalog:
            if boost_card.get_rarity() == boost_rarity:
                if len(eligible_cards) < boost_count:
                    eligible_cards.append(boost_card)

        if len(eligible_cards) > 0:
            r_set_base = self.parse_page(set_base_card_url)
            if r_set_base:
                # read the HTML to confirm base is right

                unique_id_url_str = "_".join(eligible_cards)
                boost_confirm_url = "http://ultimate-a.cygames.jp/ultimate/app_manage/post_redirection/?url=card_str%2Fstrengthen%2F" + unique_id_url_str
                post_data = {'sleevestr': unique_id_url_str}

                r_boost_confirm = self.parse_page(boost_confirm_url, req="post", payload=post_data)
                if r_boost_confirm:
                    # read HTML to confirm base is right

                    #success!

                    self.update_cards()

        return base_card
