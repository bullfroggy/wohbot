import optparse
from player import Player
from bot import Bot
from woh import WoH


def run(sid):
    player_settings = {
        "sid": sid,
    }
    player = Player(player_settings)

    bot_settings = {
        "player": player,
    }
    bot = Bot(bot_settings)

    bot.max_farm_newest_mission()


def main():
    p = optparse.OptionParser()
    p.add_option('--sid', '-s', default="")
    options, arguments = p.parse_args()

    if not options.sid:
        print "Please enter your SID:"
        options.sid = raw_input()
    
    run(options.sid)

if __name__ == '__main__':
    main()