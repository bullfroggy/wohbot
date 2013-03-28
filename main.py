import optparse
from bot import Bot


class Woh(object):
    settings = {
        "farm_mission": "23",
        "urls": {


        }
    }

def main():
    p = optparse.OptionParser()
    p.add_option('--sid', '-s', default="")
    p.add_option('--farm_mission', '-f', default="23")
    options, arguments = p.parse_args()
    settings = {
        "sid": options.sid,
        "farm_mission": options.farm_mission,

    }
    bot = Bot(settings)
    #bot.update_roster()
    bot.max_farm()
    # Adding a second maxFarm to catch the Levelups.  Should be done better at a later time
    bot.max_farm()
    print "Done!"

if __name__ == '__main__':
       main()