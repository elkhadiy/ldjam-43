import random
import datetime
import time
from pprint import pprint
from ulis43.game import Game


def run():
    random.seed(datetime.datetime.now())

    g = Game()
    pprint(g, indent=4)

    print("-======== GAME LOOP ========-")
    while True:
        g.tick()
        pprint(g.spaceship.ressources)
        time.sleep(1)


if __name__ == '__main__':
    run()
