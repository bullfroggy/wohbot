import re
from woh import WoH

class CommonEqualityMixin(object):

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.get_unique_id() == other.get_unique_id())

    def __ne__(self, other):
        return not self.__eq__(other)

class Card(CommonEqualityMixin):
    unique_id = None

    def __init__(self, player, unique_id, properties):
        self.player = player
        self.woh = WoH(player)
        self.unique_id = unique_id
        self.properties = properties

    def __eq__(self, other):
        return self.get_unique_id() == other.get_unique_id()

    def __hash__(self):
        return hash(('unique_id', self.get_unique_id()))

    def set_unique_id(self, unique_id):
        self.unique_id = unique_id

    def set_global_id(self, global_id):
        self.properties.update({"global_id": global_id})

    def set_img_id(self, img_id):
        self.properties.update({"img_id": img_id})

    def set_name(self, img_id):
        self.properties.update({"name": name})

    def set_rarity(self, rarity):
        self.properties.update({"rarity": rarity})

    def set_alignment(self, alignment):
        self.properties.update({"alignment": alignment})

    def set_max_level(self, max_level):
        self.properties.update({"max_level": max_level})

    def set_level(self, level):
        self.properties.update({"level": level})

    def set_ability_level(self, ability_level):
        self.properties.update({"ability_level": ability_level})

    def set_atk_pwr(self, atk_pwr):
        self.properties.update({"atk_pwr": atk_pwr})

    def set_def_pwr(self, def_pwr):
        self.properties.update({"def_pwr": def_pwr})

    def set_pwr_req(self, pwr_req):
        self.properties.update({"pwr_req": pwr_req})

    def set_silver(self, silver):
        self.properties.update({"silver": silver})

    def get_global_id(self):
        return self.properties["global_id"]

    def get_img_id(self):
        return self.properties["img_id"]

    def get_name(self):
        return self.properties["name"]

    def get_unique_id(self):
        return self.unique_id

    def get_rarity(self):
        return self.properties["rarity"]

    def get_alignment(self):
        return self.properties["alignment"]

    def get_max_level(self):
        return self.properties["max_level"]

    def get_level(self):
        return self.properties["level"]

    def get_ability_level(self):
        return self.properties["ability_level"]

    def get_atk_pwr(self):
        return self.properties["atk_pwr"]

    def get_def_pwr(self):
        return self.properties["def_pwr"]

    def get_pwr_req(self):
        return self.properties["pwr_req"]

    def get_silver(self):
        return self.properties["silver"]

    def get_base_rarity(self):
        return int(str(self.properties["global_id"])[2:3])

    def get_version(self):
        return int(str(self.properties["global_id"])[-1])

    def fuse(self, fuser_card):
        new_card = self

        if isinstance(fuser_card, Card):
            fuser_id = fuser_card.get_unique_id()
        else:
            fuser_id = str(fuser_card)

        r_set_base_url = self.woh.URLS['fuse_base_set'] + self.get_unique_id()
        print r_set_base_url
        r_set_base = self.woh.parse_page(r_set_base_url)
        if r_set_base:
            print "Base fuse set to " + self.get_name()
            #read page HTML to ensure base card is what we expect
            #success!
            r_fuse_card_url = self.woh.URLS['fuse_card_set'] % (fuser_id, fuser_id)
            print r_fuse_card_url
            r_fuse_card = self.woh.parse_page(r_fuse_card_url)
            if r_fuse_card:
                #read page HTML to get success message
                r_fuse_result = self.woh.parse_page(self.woh.URLS['card_list_desc'] + self.get_unique_id())
                if r_fuse_result:
                    #TODO: Get follow up to parse image properly
                    card_img = r_fuse_result.select("img[src^='http://ultimate-a.cygames.jp/ultimate/image_sp/en/card/']")
                    card_info = r_fuse_result.select(".userLeft")[0]
                    print repr(card_img)
                    if card_img and card_info:
                        image_id = re.search(r"\/card\/\w+\/([a-f0-9]+)\.jpg", card_img.get("src").strip()).group(1)
                        global_properties = self.woh.parse_card_json(image_id)

                        new_level = int(re.search(r"Lv: (\d+)\/", card_info.get_text().strip()).group(1))

                        properties = {
                            "global_id": global_properties["global_id"],
                            "img_id": image_id,
                            "name": global_properties["name"],
                            "rarity": global_properties["rarity"],
                            "alignment": global_properties["alignment"],
                            "pwr_req": global_properties["power_required"],
                            "level": new_level,
                        }
                        # Make a new card object with the given information
                        new_card = Card(self.get_unique_id(), properties)

                        if new_card.get_rarity() > self.get_rarity():
                            print "Successfully fused base card %s to fuser %s" % (self.get_unique_id(), fuser_card)
                        #double success!
                        # if success, remove fuser card from roster
                pass
            #raw_input("press enter to continue...")
        return new_card

    def boost(self, boosters=[]):
        if len(boosters) > 0:
            r_set_base_url = self.woh.URLS['boost_base_set'] + self.get_unique_id()
            print "Boosting " + self.get_name() 
            r_set_base = self.woh.parse_page(r_set_base_url)
            if r_set_base:
                # TODO: read the HTML to confirm base is right
                unique_id_url_str = "_".join(map(str, boosters))
                r_boost_url = self.woh.URLS['boost_card_set'] + unique_id_url_str
                print r_boost_url

                r_boost_confirm = self.woh.parse_page(r_boost_url)

                r_boost_result = self.woh.parse_page(self.woh.URLS['card_list_desc'] + self.get_unique_id())
                if r_boost_result:
                    card_info = r_boost_result.select(".userLeft")[0]
                    #print card_info
                    if card_info:
                        new_level = int(re.search(r"Lv: (\d+)\/", card_info.get_text().strip()).group(1))
                        # TODO: read HTML to confirm boost occurred
                        # Update self level in roster
                        print "Base card level is now at " + str(new_level)
                        self.set_level(new_level)
                        pass
                        #success!
        #raw_input("Press Enter to continue...")
        return self
