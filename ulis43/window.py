import pygame
from pygame.locals import *

import yaml

import ulis43
from ulis43.asset_manager import AssetManager


class Window():

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((800, 600))

        AssetManager().loadFont("hud", "Lunchds/lunchds.ttf", 18)
        AssetManager().loadFont("title", "Andromeda/AndromedaTV.TTF", 32)

        rooms_folder = ulis43.basedir / "res" / "images" / "rooms"
        for room in rooms_folder.iterdir():
            AssetManager().loadImage(room.stem, "rooms/" + room.name)

        res_folder = ulis43.basedir / "res"
        crew_appearance_file = res_folder / "crew_appearance.yaml"
        with crew_appearance_file.open() as f:
            crew_appearance = yaml.safe_load(f)

        for folder in crew_appearance["images"]:
            for file in crew_appearance["images"][folder]:
                name = str(folder) + "_" + str(file)
                path = "crews/" + str(folder) + "/" + str(file) + ".png"
                AssetManager().loadImage(name, path)

    def draw(self, game):

        self.window.fill((0, 0, 0))

        game.spaceship.draw(self.window)

        pygame.display.flip()
