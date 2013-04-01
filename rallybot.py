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
    points = player.getRallyPoints()
    available = player.CardAvailable()
    print "free card pack available:", available
    if available:
        player.freeRallyPack()
    print points, "rally points"
    print "rallying players"
    player.rallyAll()
    time.sleep(3)
    points = player.getRallyPoints()
    print points, "rally points"
    if points / 200 >= 1:
        cart = points / 200
        print "attempting to buy", cart, "rally packs"
        player.buyRallyPacks(cart)
    else:
        print "not buying"
    time.sleep(3)
    points = player.getRallyPoints()
    print points, "rally points"
    print "Done!"

if __name__ == '__main__':
    main()
