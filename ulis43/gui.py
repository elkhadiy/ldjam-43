import random
import datetime
import multiprocessing
import time

from ulis43.game import Game
from ulis43.window import Window


def logic_worker(g):
    while True:
        g.tick()
        # print(g.spaceship.ressources)
        time.sleep(1)


def draw_worker(window, g):
    while True:
        window.draw(g)


def run():
    random.seed(datetime.datetime.now())
    g = Game()
    window = Window()

    logic_job = multiprocessing.Process(target=logic_worker, args=(g,))
    draw_job = multiprocessing.Process(target=draw_worker, args=(window, g))

    logic_job.start()
    draw_job.start()


if __name__ == '__main__':
    run()
