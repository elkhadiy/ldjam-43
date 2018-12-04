import pygame
import pygame.freetype
from pygame.mixer import *

import ulis43


class AssetManager(object):
    class __AssetManager:
        def __init__(self):
            self.images = {}
            self.coloredImages = {}

            self.sounds = {}
            self.musics = {}
            self.fonts = {}

            self.currentMusic = None


            pygame.mixer.pre_init(44100, 16, 2, 4096)
            pygame.mixer.init()

            # Reserve one channel for music
            pygame.mixer.set_reserved(1)

            pygame.freetype.init()

        def loadImage(self, name, path, scale=1):
            img = pygame.image.load( str(ulis43.basedir / "res" / "images" / path) ).convert_alpha()

            if scale == 1:
                self.images[name] = img
            elif scale == 2:
                self.images[name] = pygame.transform.scale2x(img)
            else:
                width, height = img.get_size()
                self.images[name] = pygame.transform.scale(img, (scale * width, scale * height))

        def loadSound(self, name, path):
            self.sounds[name] = pygame.mixer.Sound( str(ulis43.basedir / "res" / "sounds" / path) )

        def loadMusic(self, name, path):
            self.musics[name] =  str(ulis43.basedir / "res" / "musics" / path)

        def loadFont(self, name, path, size):
            self.fonts[name] = pygame.freetype.Font(str(ulis43.basedir / "res" / "fonts" / path), size)


        def playMusic(self, name):
            if (self.currentMusic != self.musics[name]):
                if self.currentMusic:
                    pygame.mixer.music.fadeout(100)
                pygame.mixer.music.load(self.musics[name])
                pygame.mixer.music.play(-1)
                self.currentMusic = self.musics[name]

        def playSound(self, name):
            self.sounds[name].play()

        def getImage(self, name):
            return self.images[name]

        def getColoredImage(self, name, color):
            if (name + str(color) in self.coloredImages.keys()) :
                image = self.coloredImages[name + str(color)]
            else :
                image = self.images[name].copy()
                w, h = image.get_size()
                for x in range(w):
                    for y in range(h):
                        prev = image.get_at((x, y))
                        image.set_at((x, y), pygame.Color(
                            (color[0] * prev[0]) // 255,
                            (color[1] * prev[1]) // 255,
                            (color[2] * prev[2]) // 255,
                            prev[3]))
                self.coloredImages[name + str(color)] = image
            return image

        def getFont(self, name):
            return self.fonts[name]

    instance = None

    def __new__(cls): # __new__ always a classmethod
        if not AssetManager.instance:
            AssetManager.instance = AssetManager.__AssetManager()
        return AssetManager.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)
