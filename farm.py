import optparse
from player import Player
from bot import Bot


def init_bot(sid):
    player_settings = {
        "sid": sid,
    }
    player = Player(player_settings)

    bot_settings = {
        "player": player,
    }
    return Bot(bot_settings)


def max_farm(bot, operation=0, mission=0):
    has_energy = True
    while has_energy:
        has_energy = bot.farm_mission(operation, mission)
        print "Farmed Mission %d-%d" % (operation, mission)


def main():
    p = optparse.OptionParser()
    p.add_option('--sid', '-s', default="")
    p.add_option('--operation', '-o', default=0)
    p.add_option('--mission', '-m', default=0)
    options, arguments = p.parse_args()

    if not options.sid:
        print "Please enter your SID:"
        options.sid = raw_input()

    bot = init_bot(options.sid)
    bot.smart_fuse()
    bot.smart_boost()
    max_farm(bot, int(options.operation), int(options.mission))
    bot.smart_fuse()
    bot.smart_boost()

if __name__ == '__main__':
    main()