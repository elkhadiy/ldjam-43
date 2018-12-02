import random
import datetime
from ulis43.game import Game
from ulis43.window import Window

def run():
    random.seed(datetime.datetime.now())
    g = Game()
    window = Window()

    while 1:
        #g.tick()
        window.draw(g)


if __name__ == '__main__':
    run()
