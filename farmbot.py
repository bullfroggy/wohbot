import optparse
from player import Player
from bot import Bot


def main():
    p = optparse.OptionParser()
    p.add_option('--sid', '-s', default="")
    p.add_option('--operation', '-o', default=2)
    p.add_option('--mission', '-m', default=3)
    options, arguments = p.parse_args()

    if not options.sid:
        print "Please enter your SID:"
        options.sid = raw_input()

    player_settings = {
        "sid": options.sid,

    }
    player = Player(player_settings)
    bot_settings = {
        "player": player,
    }
    bot = Bot(bot_settings)
    bot.max_farm(options.operation, options.mission)
    # Adding a second maxFarm to catch the Levelups.  Should be done better at a later time
    bot.max_farm(options.operation, options.mission)
    print "Done!"

if __name__ == '__main__':
       main()