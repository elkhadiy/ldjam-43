import pygame
from pygame.locals import *

from ulis43.asset_manager import AssetManager
from ulis43.gui import GUI

class Window():

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((800, 600))

        AssetManager().loadImage("water", "rooms/water.png")
        AssetManager().loadImage("farm", "rooms/farm.png")

        AssetManager().loadImage("body_1", "crews/bodies/Skinny.png")

    def draw(self, game):
        water = AssetManager().getImage("water")
        farm = AssetManager().getImage("farm")
        for j in range(0, 5):
            for i in range(0, 5):
                 self.window.blit(water, (i*100,j*100)) if (i+j%2) else self.window.blit(farm, (i*100,j*100))

        body = AssetManager.getImageColored("body_1", (255,0,0))


        pygame.display.flip()
