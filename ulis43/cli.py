import random
import datetime
import time

from ulis43.game import Game


def run():
    random.seed(datetime.datetime.now())

    g = Game()
    for room in g.spaceship.rooms:
        print(room.type, ":")
        for p in room.staff:
            print("\t", p.name, ":", p.skills)

    print("-======== GAME LOOP ========-")
    while True:
        g.tick()
        print(g.spaceship.ressources)
        time.sleep(1)


if __name__ == '__main__':
    run()
