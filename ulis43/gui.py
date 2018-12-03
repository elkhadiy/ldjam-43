import argparse
import random
import datetime
import pygame.time
from pygame.locals import *

from ulis43.game import Game
from ulis43.title_screen import TitleScreen
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
    title_screen = TitleScreen()
    g = Game()
    window = Window()

    delta = 0
    quit = False
    start = False
    event = None
    pos = None

    while not (start or quit):
        for event in pygame.event.get():
            if event.type == QUIT:
                quit = True
            elif event.type == MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                title_screen.click_event(pos, "down")
            elif event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                start = title_screen.click_event(pos, "up")
        window.draw(title_screen)

    while not quit:
        for event in pygame.event.get():
            if event.type == QUIT:
                print("SEED:", seed)
                quit = True
            # MOUSEBUTTONUP on it's own seems unreliable
            elif event.type == MOUSEBUTTONDOWN or event.type == MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                event = "CLICK"

        before = pygame.time.get_ticks()
        while delta > 200:
            g.tick(event, pos)
            delta -= 200
        window.draw(g)
        exectime = pygame.time.get_ticks() - before
        pygame.time.delay(17 - exectime)
        delta += max(exectime, 17)


if __name__ == '__main__':
    run()
