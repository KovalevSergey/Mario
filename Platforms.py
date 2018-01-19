# -*- coding: utf-8 -*-
#
from pygame.sprite import Sprite
from pygame.image import load

 #Классы основных платформ
class Platform(Sprite):
    def __init__(self, x, y): #Конструкция класса
        Sprite.__init__(self)
        self.image = load("blocks/floor.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Block(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = load("blocks/block.png")

class Radius(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = load("blocks/r.png")

class Floor(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = load("blocks/floor1.png")

class BlockDie(Platform): #Класс шипы
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = load("blocks/spikes.png")
class Water(Platform): #Класс вода
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = load("blocks/water.png")
class Lava(Platform): #Класс лава
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = load("blocks/lava.png")

class Teleport(Platform): #Класс телепорт
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = load("blocks/portal.png")

class Exit(Platform): #Класс финиш
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = load("blocks/exit.png")