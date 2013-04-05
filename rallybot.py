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
    # available = player.card_available()
    points = player.get_rally_points()
    print points, "rally points"
    # print "Free card pack available:", available
    # remainder = player.get_card_space_remaining()
    # if available:
    #     if remainder > 0:
    #         player.free_rally_pack()
    #     else:
    #         print "No remaining card space"
    # remainder = player.get_card_space_remaining()
    # if points / 200 >= 1:
    #     cart = points / 200
    #     if remainder > 0:
    #         if remainder < cart:
    #             cart = remainder
    #         print "Attempting to buy", cart, "rally packs"
    #         player.buy_rally_packs(cart)
    #         points = player.get_rally_points()
    #         print points, "rally points"
    # print "Rallying players"
    # player.rally_all()
    # #time.sleep(3)
    # points = player.get_rally_points()
    # print points, "rally points"
    # remainder = player.get_card_space_remaining()
    # if points / 200 >= 1:
    #     cart = points / 200
    #     if remainder > 0:
    #         if remainder < cart:
    #             cart = remainder
    #         print "Attempting to buy", cart, "rally packs"
    #         player.buy_rally_packs(cart)
    #         points = player.get_rally_points()
    #         print points, "rally points"
    # else:
    #     print "Not buying"
    #time.sleep(3)
    print "Rallying Players"
    player.message_all()
    points = player.get_rally_points()
    print points, "rally points"
    print "Done!"

if __name__ == '__main__':
    main()
