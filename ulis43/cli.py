import random
import datetime
from ulis43.game import Game


def run():
    random.seed(datetime.datetime.now())
    g = Game()
    print(g)


if __name__ == '__main__':
    run()
