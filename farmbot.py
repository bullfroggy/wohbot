import optparse
from player import Player
from bot import Bot


def main():
    p = optparse.OptionParser()
    p.add_option('--sid', '-s', default="")
    p.add_option('--farm_mission', '-f', default="mission_23")
    options, arguments = p.parse_args()

    if not options.sid:
        print "Please Enter you SID:"
        options.sid = raw_input()

    player_settings = {
        "sid": "",
        "farm_mission": options.farm_mission,

    }
    player = Player(player_settings)
    bot_settings = {
        "player": player,
    }
    bot = Bot(bot_settings)
    bot.max_farm()
    # Adding a second maxFarm to catch the Levelups.  Should be done better at a later time
    bot.max_farm()
    print "Done!"

if __name__ == '__main__':
       main()