import optparse
from player import Player
from bot import Bot


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
    points = player.getRallyPoints()
    print points, "rally points"
    print "rallying players"
    bot.randRally()
    if points / 200 > 1:
        cart = points / 200
        print "buying", cart, "cards"
        player.buyRallyPacks(cart)
    else:
        print "not buying"
    available = player.CardAvailable()
    print "free card pack available:", available
    if available:
        player.freeRallyPack()
    points = player.getRallyPoints()
    print points, "rally points"
    print "Done!"

if __name__ == '__main__':
    main()
