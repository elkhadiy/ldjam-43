import argparse
import random
import datetime
import pygame.time
from pygame.locals import *

from ulis43.game import Game
from ulis43.window import Window


def run():
    parser = argparse.ArgumentParser(prog='ulis43')
    parser.add_argument('-s', '--seed', help='ship seed')
    args = parser.parse_args()
    if not args.seed:
        seed = str(datetime.datetime.now())
    else:
        seed = args.seed
    random.seed(seed)
    g = Game()
    window = Window()

    delta = 0
    quit = False
    event = None
    pos = None

    while not quit:
        for event_ in pygame.event.get():
            if event_.type == QUIT:
                print("SEED:", seed)
                quit = True


        before = pygame.time.get_ticks()
        while delta > 1000:
            g.tick()
            delta -= 1000
        window.draw(g)
        exectime = pygame.time.get_ticks() - before
        pygame.time.delay(17 - exectime)
        delta += max(exectime, 17)


if __name__ == '__main__':
    run()
