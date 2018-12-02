import pygame
from pygame.locals import *

from ulis43.asset_manager import AssetManager


class Window():

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((800, 600))

        AssetManager().loadImage("water", "rooms/Water.png")
        AssetManager().loadImage("farm", "rooms/Farm.png")

    def draw(self, game):
        water = AssetManager().getImage("water")
        farm = AssetManager().getImage("farm")
        for j in range(0, 5):
            for i in range(0, 5):
                self.window.blit(water, (i*100,j*100)) if (i+j%2) else self.window.blit(farm, (i*100,j*100))

        pygame.display.flip()
