import argparse
import random
import datetime
import pygame.time
from pygame.locals import *

from ulis43.game import Game
from ulis43.title_screen import TitleScreen
from ulis43.gameover_screen import GameOverScreen
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
    gameover_screen = GameOverScreen()
    window = Window()

    tick_rate = 250

    delta = 0
    quit = False
    start = False
    gameover = False
    restart = True
    event = None
    pos = None
    g = Game()

    while restart and not quit:

        while not (start or quit):
            for event_ in pygame.event.get():
                if event_.type == QUIT:
                    quit = True
                elif event_.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    title_screen.click_event(pos, "down")
                elif event_.type == MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    start = title_screen.click_event(pos, "up")
            window.draw(title_screen)

        while not (quit or gameover):
            for event_ in pygame.event.get():
                if event_.type == QUIT:
                    print("SEED:", seed)
                    quit = True

            before = pygame.time.get_ticks()
            while delta > tick_rate:
                gameover = g.tick()
                delta -= tick_rate
            window.draw(g)
            exectime = pygame.time.get_ticks() - before
            pygame.time.delay(17 - exectime)
            delta += max(exectime, 17)

        restart = False

        while not quit and not restart:
            for event_ in pygame.event.get():
                if event_.type == QUIT:
                    print("SEED:", seed)
                    quit = True
                elif event_.type == MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    gameover_screen.click_event(pos, "down")
                elif event_.type == MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    restart = gameover_screen.click_event(pos, "up")
            window.draw(gameover_screen)

        delta = 0
        start = False
        gameover = False
        restart = True
        pos = None
        g = Game()
        title_screen.start = False
        gameover_screen.start = False


if __name__ == '__main__':
    run()
