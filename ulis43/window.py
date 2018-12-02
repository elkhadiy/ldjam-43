import pygame
from pygame.locals import *

from ulis43.asset_manager import AssetManager


class Window():

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((800, 600))

        AssetManager().loadImage("water", "rooms/Water.png")
        AssetManager().loadImage("farm", "rooms/Farm.png")

        AssetManager().loadFont("vera", "Vera/VeraMoBd.ttf", 16)

    def draw(self, game, delta=None):

        self.window.fill((0, 0, 0))

        game.draw(self.window)

        pygame.display.flip()
