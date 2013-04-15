import re
from card import Card
from woh import WoH

class CommonEqualityMixin(object):

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.get_unique_id() == other.get_unique_id())

    def __ne__(self, other):
        return not self.__eq__(other)

class Present(CommonEqualityMixin):
    present_id = None
    TYPES = {
        "card": 0,
        "silver": 1,
        "item": 2,
        "rally": 3,
    }

    def __init__(self, player, present_id, timestamp='', auth_type=1, type="card", note="", card_properties=dict('',)):
        self.player = player
        self.woh = WoH(player)
        self.present_id = present_id
        self.quantity = quantity
        self.timestamp = timestamp
        self.auth_type = auth_type
        self.type = self.TYPES[present_type]
        self.note = note
        self.properties = properties

    def __eq__(self, other):
        return self.get_unique_id() == other.get_unique_id()

    def __hash__(self):
        return hash(('unique_id', self.get_unique_id()))

    def set_present_id(self, present_id):
        self.present_id = present_id

    def set_img_id(self, img_id):
        self.properties.update({"img_id": img_id})

    def set_global_id(self, global_id):
        self.properties.update({"global_id": global_id})


    def get_rally_points(self):
        if self.type == self.TYPES["rally"]:
            return self.properties["points"]
        else:
            return False

    def get_silver(self):
        if self.type == self.TYPES["silver"]:
            return self.properties["silver"]
        else:
            return False

    def get_global_id(self):
        if self.type == self.TYPES["card"]:
            return self.properties["global_id"]
        else:
            return False

    def get_global_id(self):
        return self.properties["global_id"]

    def get_img_id(self):
        return self.properties["img_id"]

    def get_note(self):
        return self.note

    def get_auth_type(self):
        return self.auth_type

    def get_present_id(self):
        return self.present_id

    def claim(self):

        claim_present_url = self.woh.URLS["present_claim"]

        html = self.woh.parse_page(claim_present_url, req="post", payload={"revieve_id": self.present_id, "view_auth_type": self.auth_type } )
        if html:
            result = True

            if self.type == self.TYPES["card"]:
                # TODO search page for confirmation of claim
                # TODO get newest collected card unique_id and return that
                pass
        else:
            result = False

        return result

