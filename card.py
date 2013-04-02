class Card(object):
    properties = {
        "global_id": "",
        "img_id": "",
        "alignment": 1,
        "rarity": 0,
        "max_level": 99,
        "level": 1,
        "ability_level": 1,
        "atk_pwr": None,
        "def_pwr": None,
        "pwr_req": None,
        "silver": 0,
        "xp": 0,
    }

    def __init__(self, unique_id, properties):
        self.unique_id = unique_id
        self.properties.update(properties)

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

    def fuse(self, fuser_card):
        r_set_base = self.woh.parse_page(self.woh.URLS['fuse_base_set'] + self.get_unique_id())
        if r_set_base:
            #read page HTML to ensure base card is what we expect
            #success!
            r_fuse_card = self.woh.parse_page(self.woh.URLS['fuse_card_set'] + fuser_card, payload=dict({'sleeve_str': fuser_card}))
            if r_fuse_card:
                #read page HTML to get success message
                #double success!
                pass



