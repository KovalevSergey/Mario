# -*- coding: utf-8 -*-
#
from pygame.sprite import Sprite, collide_rect
from pygame import Surface, mixer
import pyganim
import Platforms
#Необходимы для работы задержки времени
from pygame import *
import os

mixer.pre_init(44100, -16, 1, 512) #Частота звука, канал, буфер
mixer.init()

MOVE_SPEED = 4.5 #Скорость передвижения
JUMPING = 7.8 #Сила прыжка
GRAVITY = 0.5 #Сила притяжения
COLOR = (77, 178, 255) #Цвета по-умолчанию

ANIMATION_DELAY = 0.1 #Задержка анимации
ANIMATION_STAY = [('player/stay.png', ANIMATION_DELAY)] #Спрайт простоя персонажа

ANIMATION_RIGHT = ['player/right.png', #Анимация бега вправо
                   'player/right1.png',
                   'player/right2.png',
                   'player/right3.png']
ANIMATION_LEFT = ['player/left.png', #Анимация бега влево
                   'player/left.png',
                   'player/left2.png',
                   'player/left3.png']

ANIMATION_UP = ['player/jump.png'] #Спрайт прыжка вверх
ANIMATION_UP_LEFT = ['player/jump_left.png'] #Спрайт прыжка влево
ANIMATION_UP_RIGHT = ['player/jump_right.png'] #Спрайт прыжка вправо


class Player(Sprite): #Класс персонажа
    def __init__(self, x, y):
        Sprite.__init__(self)
        self.image = Surface((23, 30))
        self.xvel = 100
        self.yvel = 350
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.onGround = False
        self.image.set_colorkey((0, 0, 0))

        def make_boltAnim(anim_list, delay): #Свойство анимации
            boltAnim = []
            for anim in anim_list:
                boltAnim.append((anim, delay))
            Anim = pyganim.PygAnimation(boltAnim)
            return Anim

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY) #Свойство - анимация простоя
        self.boltAnimStay.play() #Запускаем анимацию

        self.boltAnimRight = make_boltAnim(ANIMATION_RIGHT, ANIMATION_DELAY) #Свойство - анимация движения враво
        self.boltAnimRight.play()#Запускаем анимацию

        self.boltAnimLeft = make_boltAnim(ANIMATION_LEFT, ANIMATION_DELAY) #Свойство - анимация движения влево
        self.boltAnimLeft.play() #Запускаем анимацию

        self.boltAnimUp = make_boltAnim(ANIMATION_UP, ANIMATION_DELAY) #Свойство - анимация прыжка
        self.boltAnimUp.play() #Запускаем анимацию
        self.jump_sound = mixer.Sound('jump.ogg') #Звук при прыжке

        self.boltAnimUpLeft = make_boltAnim(ANIMATION_UP_LEFT, ANIMATION_DELAY) #Свойство - спрайт прыжка влево
        self.boltAnimUpLeft.play() #Запускаем анимацию

        self.boltAnimUpRight = make_boltAnim(ANIMATION_UP_RIGHT, ANIMATION_DELAY) #Свойство - спрайт прыжка вправо
        self.boltAnimUpRight.play() #Запускаем анимацию
        self.winner = False

    def update(self, left, right, up, platforms):
        if up: #Свойство прыжка
            if self.onGround:
                self.yvel = -JUMPING
                self.jump_sound.play() #Для прыжка, чтобы звук шел только 1 раз
            self.image.fill(COLOR)
            self.boltAnimUp.blit(self.image, (0, 0))

        if left: #Свойство передвижения влево
            self.xvel = -MOVE_SPEED
            self.image.fill(COLOR)
            if up: #Анимация для прыжка влево
               self.boltAnimUpLeft.blit(self.image, (0, 0))
            else:
               self.boltAnimLeft.blit(self.image, (0, 0))

        if right: #Свойство передвижения враво
            self.xvel = MOVE_SPEED
            self.image.fill(COLOR)
            if up: #Анимация для прыжка вправо
               self.boltAnimUpRight.blit(self.image, (0, 0))
            else:
               self.boltAnimRight.blit(self.image, (0, 0))

        if not (left or right): #Стоим, если не указан путь
            self.xvel = 0
            if not up:
                self.image.fill(COLOR)
                self.boltAnimStay.blit(self.image, (0, 0))
        if not self.onGround:
            self.yvel += GRAVITY

        self.onGround = False
        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

    def collide(self, xvel, yvel, platforms): #Метод для обнаружения столкновения героя с платформой
        for pl in platforms:
            if collide_rect(self, pl):
                if isinstance(pl, Platforms.BlockDie) or isinstance(pl, Platforms.Water) or isinstance(pl, Platforms.Lava):  #Если пересекаем шипы
                    self.die()  #Умираем
                elif isinstance(pl, Platforms.Teleport):  #Если пересекаем телепорт
                    self.tl() #Перемещаемся
                elif isinstance(pl, Platforms.Exit):  #При контакте с призом
                    self.winner = True
                    print ('МОЛОДЕЦ!!!')#Побеждаем
                else:
                 if xvel > 0:
                    self.rect.right = pl.rect.left
                 if xvel < 0:
                    self.rect.left = pl.rect.right
                 if yvel > 0:
                    self.rect.bottom = pl.rect.top
                    self.onGround = True
                    self. yvel = 0
                 if yvel < 0:
                    self.rect.top = pl.rect.bottom
                    self.yvel = 0

    def teleporting(self, xvel, yvel): #Координаты после смерти
        self.rect.x = 50
        self.rect.y = 500

    def die(self): #Свойство смерти
        time.wait(100) #Задержка после смерти
        self.teleporting(self.xvel, self.yvel)

    def teleport(self, xvel, yvel): #Координаты телепорта
            self.rect.x = 3000
            self.rect.y = 10

    def tl(self): #Свойство телепорта
        time.wait(500) #Задержка при телепортации
        self.teleport(self.xvel, self.yvel)