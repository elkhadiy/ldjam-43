import pygame
from pygame.locals import *

import yaml

import ulis43
from ulis43.asset_manager import AssetManager

class Window():

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((800, 600))

        AssetManager().loadImage("water", "rooms/Water.png")
        AssetManager().loadImage("farm", "rooms/Farm.png")
        AssetManager().loadImage("electricity", "rooms/Electricity.png")


        res_folder = ulis43.basedir / "res"
        crew_appearance_file = res_folder / "crew_appearance.yaml"
        with crew_appearance_file.open() as f:
            crew_appearance = yaml.safe_load(f)

        for folder in crew_appearance["images"]:
            print(folder)
            for file in crew_appearance["images"][folder]:
                name = str(folder) + "_" + str(file)
                path = "crews/" + str(folder) + "/" + str(file) + ".png"
                print (name, path)
                AssetManager().loadImage( name, path )



    def draw(self, game):
        water = AssetManager().getImage("water")
        farm = AssetManager().getImage("farm")
        for j in range(0, 5):
            for i in range(0, 5):
                 self.window.blit(water, (i*100,j*100)) if (i+j%2) else self.window.blit(farm, (i*100,j*100))

        game.spaceship.draw(self.window)

        pygame.display.flip()
