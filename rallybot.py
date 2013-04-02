import optparse
from player import Player
import time

def main():
    p = optparse.OptionParser()
    p.add_option('--sid', '-s', default="")
    p.add_option('--farm_mission', '-f', default="mission_23")
    options, arguments = p.parse_args()
    player_settings = {
        "sid": options.sid,
        "farm_mission": options.farm_mission
    }
    player = Player(player_settings)
    points = player.get_rally_points()
    available = player.card_available()
    print "free card pack available:", available
    remainder = player.get_card_space_remaining()
    if remainder > 0:
        if available:
            player.free_rally_pack()
    print points, "rally points"
    if points / 200 >= 1:
        cart = points / 200
        if remainder > 0:
            if remainder < cart:
                cart = remainder
            print "attempting to buy", cart, "rally packs"
            player.buy_rally_packs(cart)
    print "rallying players"
    player.rally_all()
    time.sleep(3)
    points = player.get_rally_points()
    print points, "rally points"
    if points / 200 >= 1:
        cart = points / 200
        if remainder > 0:
            if remainder < cart:
                cart = remainder
            print "attempting to buy", cart, "rally packs"
            player.buy_rally_packs(cart)
    else:
        print "not buying"
    time.sleep(3)
    points = player.get_rally_points()
    print points, "rally points"
    print "Done!"

if __name__ == '__main__':
    main()
