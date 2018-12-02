import pygame
import ulis43

class AssetManager(object):
    class __AssetManager:
        def __init__(self):
            self.images = {}
            self.sounds = {}
            self.musics = {}
            self.fonts = {}

            self.currentMusic = None


            pygame.mixer.pre_init(44100, 16, 2, 4096)
            pygame.mixer.init()

            # Reserve one channel for music
            pygame.mixer.set_reserved(1)

            pygame.font.init()

        def loadImage(self, name, path):
            self.images[name] = pygame.image.load( str(ulis43.basedir / "res" / "images" / path) ).convert()

        def loadSound(self, name, path):
            self.sounds[name] = pygame.mixer.Sound( str(ulis43.basedir / "res" / "sounds" / path) )

        def loadMusic(self, name, path):
            self.musics[name] = pygame.mixer.music( str(ulis43.basedir / "res" / "musics" / path) )

        def loadFont(self, name, path, size):
            self.fonts[name] = pygame.font.Font(str(ulis43.basedir / "res" / "fonts" / path), size)


        def playMusic(self, name):
            if (currentMusic != self.musics[name]):
                currentMusic.fadeout(100)
                self.musics[name].play(-1)
                currentMusic = self.musics[name]

        def playSound(self, name):
            self.sounds[name].play()

        def getImage(self, name):
            return self.images[name]

        def getColoredImage(self, name, color):
            image = self.images[name]
            w, h = image.get_size()
            for x in range(w):
                for y in range(h):
                    prev = image.get_at((x, y))
                    image.set_at((x, y), prev * pygame.Color(color[0], color[1], color[2], 255))

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
