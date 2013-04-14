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

    def farm_mission(self, operation, mission):
        if operation == 0 or mission == 0:
            operation, mission = self.player.get_newest_mission()

        if mission == "boss":
            self.woh.parse_page(self.woh.get_mission_url(operation, mission))
            print "Farmed Boss at %d-%s" % (operation, mission)
            return True
        else:
            if self.player.get_remaining_energy() >= self.woh.OPERATION_ENERGY_COST[operation]:
                self.woh.parse_page(self.woh.get_mission_url(operation, mission))
                print "Farmed Mission %d-%d" % (operation, mission)
                return True
            else:
                return False


    """
    This function fuses a filtered series of base_cards with a matching fuser_card.
    # fuse_alignment correlates to database alignments. 0 is any, 1 is speed, 2 is bruiser, 3 is tactics
    """
    def smart_fuse(self, fuse_rarity=1, fuse_alignment=0, max_fuse_level=0):
        fused_cards = []
        spent_ids = []

        self.player.update_fusables()
        eligible_fuse_cards = self.player.get_fusables(rarity=fuse_rarity, max_level=max_fuse_level, alignment=fuse_alignment)

        for c in eligible_fuse_cards:
            bgid = c.get_global_id()
            buid = c.get_unique_id()

            if buid not in spent_ids:
                for fc in eligible_fuse_cards:
                    fgid = fc.get_global_id()
                    fuid = fc.get_unique_id()

                    if fgid == bgid and buid != fuid and fuid not in spent_ids:
                        # Fuse base card with fuser
                        fused_card = c.fuse(fuid)
                        if fused_card.get_unique_id() == buid:
                            fused_cards.append(c)
                            spent_ids.append(buid)
                            spent_ids.append(fuid)
                        else:
                            print "Error: Fused result %s does not match expected unique ID %s" % (fused_card.get_unique_id(), buid)

        return fused_cards

    """
    This function boosts a filtered series of base_cards against a filtered series of eligible fuse_cards.
    """
    def smart_boost(self, base_rarity=2, base_version=-1, base_alignment=0, base_max_level=10, base_max_pwr_req=20, boost_rarity=0, boost_count=1, boost_alignment=0, boost_version=0, boost_max_level=1, boost_max_pwr_req=11):
        boosted_cards = []
        spent_ids = []

        # Get all requested cards
        self.player.update_roster()
        base_cards = self.player.get_roster(rarity=base_rarity, version=base_version, alignment=base_alignment, max_level=base_max_level, max_pwr_req=base_max_pwr_req)
        boost_cards = self.player.get_roster(rarity=boost_rarity, alignment=boost_alignment, version=boost_version, max_level=boost_max_level, max_pwr_req=boost_max_pwr_req)

        # Sort base cards by fused/unfused
        base_cards.sort(key=lambda c: c.get_base_rarity, reverse=True)

        # Iterate through each base card
        for curr_card in base_cards:
            card_boosted = False
            base_card = curr_card

            if len(boost_cards) >= 1:
                if base_card.get_unique_id() not in spent_ids:
                    print "Working on " + base_card.get_name() + "/lvl " + str(base_card.get_level())

                    while len(boost_cards) > 0 and base_card.get_level() <= base_max_level:
                        # Get set of matching boost cards
                        boost_set = boost_cards[:boost_count]
                        boost_ids = [bcard.get_unique_id() for bcard in boost_set]

                        print "Found " + str(len(boost_ids)) + " qualifying boosters"
                        print base_card.get_name() + " eligible for boost at lvl " + str(base_card.get_level())
                        result = base_card.boost(boost_ids)

                        if result.get_unique_id() == base_card.get_unique_id():
                            print result.get_name() + " boosted to lvl " + str(result.get_level())
                            base_card = result
                            card_boosted = True

                            # Mark used cards as spent
                            [spent_ids.append(uid) for uid in boost_ids]

                            # Remove used set of boost cards from list
                            boost_cards = boost_cards[boost_count:]

                    if card_boosted:
                        boosted_cards.append(result)
            else:
                print "No more qualifying boosters"
                break

        return boosted_cards
