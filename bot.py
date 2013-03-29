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

    def randRally(self):
        for x in range(1225, 10000):
            start = "http://ultimate-a.cygames.jp/ultimate/cheer/index/"
            end = "/1?rnd=277000578&viewer_id=null&message=Greetings+from+the+front&sort=&to_viewer_id=67417639&bef_friendship_point=102&aft_friendship_point=106&is_message=1&is_cheer=1&is_error=0&ret_act=1&message_id=&page=&offset="
            middle = x
            startU = "http://ultimate-a.cygames.jp/ultimate/profile/show/"
            endU = "?rnd=48289233&viewer_id=null"
            middleU = x
            URL = start + str(middle) + end
            userURL = startU + str(middleU) + endU
            self.woh.URLS['rally_rand'] = URL
            self.woh.URLS['user_page'] = userURL
            userPage = self.woh.parse_page(userURL)
            if userPage:
                if "An error has been detected" not in str(userPage):
                    print "player", x, "exists; attempting rally"
                    rallyURL = self.woh.parse_page(URL)
                    if "Received 4 Rally Points!" in str(rallyURL):
                        print "Successfully rallied user", x
                    else:
                        print "Could not rally user", x
                else:
                    print "player", x, "does not exist"
            else:
                return False
        return True

    def max_farm(self):
        required_battles = int(self.player.get_remaining_energy() / 3)
        self.farm(required_battles)
