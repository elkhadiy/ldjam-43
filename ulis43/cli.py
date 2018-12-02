import random
import datetime
import time

from ulis43.game import Game


def run():
    random.seed(datetime.datetime.now())

    g = Game()
    print(g)

    print("-======== GAME LOOP ========-")
    while True:
        g.tick()
        print(g.spaceship.ressources)
        time.sleep(1)


if __name__ == '__main__':
    run()
