import optparse
from player import Player
from bot import Bot
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
    bot_settings = {
        "player": player
    }
    bot = Bot(bot_settings)
    available = player.card_available()
    points = player.get_rally_points()
    print points, "rally points"
    print "Free card pack available:", available
    remainder = player.get_card_space_remaining()
    if available:
        if remainder > 0:
            bot.get_free_pack()
        else:
            print "No remaining card space"
    remainder = player.get_card_space_remaining()
    if points / 200 >= 1:
        cart = points / 200
        if remainder > 0:
            if remainder < cart:
                cart = remainder
            print "Attempting to buy", cart, "rally packs"
            bot.buy_rally_packs(cart)
            points = player.get_rally_points()
            print points, "rally points"
        print "Rallying Players"
    bot.message_friends()
    points = player.get_rally_points()
    print points, "rally points"
    remainder = player.get_card_space_remaining()
    if points / 200 >= 1:
        cart = points / 200
        if remainder > 0:
            if remainder < cart:
                cart = remainder
            print "Attempting to buy", cart, "rally packs"
            bot.buy_rally_packs(cart)
            points = player.get_rally_points()
            print points, "rally points"
    else:
        print "Not buying"
    print "Done!"

if __name__ == '__main__':
    main()
