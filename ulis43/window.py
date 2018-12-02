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

    def draw(self, game):

        self.window.fill((0, 0, 0))

        textsurface = AssetManager().getFont("vera").render(
            str(game.spaceship.ressources), False, (255, 255, 255)
            )
        self.window.blit(textsurface, (0, 0))

        pygame.display.flip()
