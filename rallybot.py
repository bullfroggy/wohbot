import optparse
from player import Player

def main():
    p = optparse.OptionParser()
    p.add_option('--sid', '-s', default="")
    options, arguments = p.parse_args()
    settings = {
        "sid": options.sid,
        }
    player = Player(settings)
    if player.getRallyPoints()/200 > 1:
        print "buying"
    else:
        print "not buying"
    print "Done!"

if __name__ == '__main__':
    main()
