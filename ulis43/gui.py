import random
import datetime
import pygame.time

from ulis43.game import Game
from ulis43.window import Window


def run():
    random.seed(datetime.datetime.now())
    g = Game()
    window = Window()

    delta = 0
    while True:
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
