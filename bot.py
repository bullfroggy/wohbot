import urls
from player import Player


class Bot(object):
    settings = {
        "sid": "",
        "farm_mission": "23",
    }

    def __init__(self, settings):
        self.settings.update(settings)
        if self.settings["farm_mission"] == "24":
            selected_mission = urls.MISSION_2_4
        else:
            selected_mission = urls.MISSION_2_3

        player_settings = {
            "sid": self.settings["sid"],
            "farm_mission": selected_mission
        }
        self.player = Player(player_settings)

    def update_roster(self):
        return self.player.update_cards()


    def max_farm(self):
        self.player.max_farm()
        return
