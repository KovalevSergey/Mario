# -*- coding: utf-8 -*-
#
import pygame
from Player import *
from Platforms import *


SIZE = (800, 600) #Размер окан
window = pygame.display.set_mode(SIZE) #Создаём окно
screen = pygame.Surface(SIZE) #Создаём игровую поверхность
pygame.display.set_caption('Mario') #Рабочее название проека

#Создаём героя
hero = Player(100,400) #Задаем положение
left = right = up = False #Основные возможности

#Уровень
level = [
         '                                                                                                                                                                              ',
         '                                                                                                                                                                              ',
         '                                                                                                               *********                                                      ',
         '                                                                                                 fffffff       fffffffff                                                      ',
         '                                                                                                 -------+      ---------                                                      ',
         '                                                                                                 -------       ---------                                                      ',
         '                                                                                                 ------l       ---------                                                      ',
         '                                                                                                 -------      +---------                                                      ',
         '                                                                                                 ---           ---------                                                      ',
         '                                                                                                 ---           ---------                                                      ',
         '                                                                                                 --- ff        ---------                                                      ',
         '                                      fff   fff                         p                        --- --f       ---------                                                      ',
         '                   ffffffffff        +---   ---                  ffffffff                        --- ---       l--------                                                      ',
         '                  f----------***      ---   ---                 f--------                        --- ---*      r                                                              ',
         'r                f-----------+++  +   ---   ---   +  +  +  +   f---------                        --- ---+      rx                                                             ',
         'r               f------------wwwwwwwww---   ---wwwwwwwwwwwwwwww----------                        --- --       +fffffffffffffffffffffffffffffffffff++++                        ',
         'r         +    f-------------wwwwwwwww---   ---wwwwwwwwwwwwwwww----------                        ---           -----------------------------------    +                       ',
         'r            *f--------------wwwwwwwww---   ---wwwwwwwwwwwwwwww----------                        ---ffff++     *----------------------------------         +                  ',
         'r     +      f---------------wwwwwwwww---   ---wwwwwwwwwwwwwwww----------                        -------      +-----------------------------------              +             ',
         'r           f----------------wwwwwwwww---   ---wwwwwwwwwwwwwwww----------                        -------                                                                      ',
         'r          f-----------------wwwwwwww----   ----wwwwwwwwwwwwwww----------                        -------                                                           +          ',
         'r         f------------------wwwwwww--       ----wwwwwwwwwwwwww----------                +       -------                                                                      ',
         'r        f-------------------wwwwww---         ---wwwwwwwwwwwww---------             +       +     -----                                                              +       ',
         'r       f--------------------wwwww--p           -----------------------                                                      +               ++    ++    +++                   ',
         'ffffffff---------------------------------lll--                             +    +                -------++    +   +   +  +    * +  +  +   +                   ++   +++        ',
         '-------------------------------------------------------------------------llllllllllllllllllllllll-------llllllllllllllllllllllfllllllllllllllllllllllllllllllllllllllllllllllllllllllll']

sprite_group = pygame.sprite.Group()
sprite_group.add(hero)
platforms = []

x = 0
y = 0
for row in level: #Обозначения для элементов постройки уровня
    for col in row:
        if col == '-':
            pl = Platform(x, y)
            sprite_group.add(pl)
            platforms.append(pl)
        if col == 'r':
            pl = Radius(x, y)
            sprite_group.add(pl)
            platforms.append(pl)
        if col == 'f':
            pl = Floor(x, y)
            sprite_group.add(pl)
            platforms.append(pl)
        if col == '+':
            pl = Block(x, y)
            sprite_group.add(pl)
            platforms.append(pl)
        if col == "*":
            pl = BlockDie(x, y)
            sprite_group.add(pl)
            platforms.append(pl)
        if col == "w":
            pl = Water(x, y)
            sprite_group.add(pl)
            platforms.append(pl)
        if col == "l":
            pl = Lava(x, y)
            sprite_group.add(pl)
            platforms.append(pl)
        if col == "p":
            pl = Teleport(x, y)
            sprite_group.add(pl)
            platforms.append(pl)
        if col == "x":
            pl = Exit(x, y)
            sprite_group.add(pl)
            platforms.append(pl)
        x += 30
    y += 30
    x = 0  # Обнуляем x, чтобы сдвинуть курсор на начало строки

#Камера
class Camera:
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pygame.Rect(0, 0, width, height)
    def apply(self, target):
        return target.rect.move(self.state.topleft)
    def  update(self, target):
        self.state = self.camera_func(self.state, target.rect)

def camera_func(camera, target_rect): #Свойство камеры
    l = -target_rect.x + SIZE[0]/2
    t = -target_rect.y + SIZE[1]/2
    w, h = camera.width, camera.height
#Камера прекращает движение, при достижении границы уровня
    l = min(0, l)
    l = max(-(camera.width-SIZE[0]), l)
    t = max(-(camera.height-SIZE[1]), t)
    t = min(0, t)

    return pygame.Rect(l, t, w, h)
total_level_width = len(level[0])*30
tottal_level_hegth = len(level)*29.5
camera = Camera(camera_func, total_level_width, tottal_level_hegth)

#Блок настройки звука
pygame.mixer.pre_init(44100, -16, 1, 512)#Частота звука, канал, буфер
pygame.mixer.init()
sound = pygame.mixer.Sound('main_theme.ogg')
sound.play(-1)#Бесконечное воспроизведение

#Открываем игровой цикл
done = True
time = pygame.time
timer = pygame.time.Clock()#FPS
while done and not hero.winner:
# Блок управления событиями
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            done = False

        if  e.type == pygame.KEYDOWN: #Нажатая клавиша
            if e.key == pygame.K_LEFT:
                left = True
            if e.key == pygame.K_RIGHT:
                right = True
            if e.key == pygame.K_UP:
                    up = True

        if e.type == pygame.KEYUP: #Не нежатая клавиша
            if e.key == pygame.K_LEFT:
                left = False
            if e.key == pygame.K_RIGHT:
                right = False
            if e.key == pygame.K_UP:
                    up = False
    #Цвет рабочей поверхности
    screen.fill((77, 178, 255))

    #Отображение героя на поверхности
    hero.update(left, right, up, platforms)
    camera.update(hero)
    for e in sprite_group:
        screen.blit(e.image, camera.apply(e))

    #Отображаем рабочую поверхность в окне
    window.blit(screen, (0, 0))
    #Обновляем окно
    pygame.display.flip()
    timer.tick(60) #Ограничение частоты кадров