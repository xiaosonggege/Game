#!/usr/bin/env python
# encoding: utf-8
'''
@author: songyunlong
@license: (C) Copyright 2020-2025.
@contact: 1243049371@qq.com
@software: pycharm
@file: virus
@time: 2020/3/23 10:31 下午
'''
import pygame
import numpy as np
from pygame.sprite import Sprite
from MainingOperation.basic_settings import Settings

def PositionInit(low:int, high:int, count:int):
    set_of_posx = np.random.randint(low=low, high=high, size=count)
    for i in set_of_posx:
        yield i

class VirusProperty:
    def __init__(self, name):
        self._name = '_' + name
    def __get__(self, instance, owner):
        return instance.__dict__[self._name]
    def __set__(self, instance, value):
        if self._name == '_ImageOfVirus':
            instance.__dict__[self._name] = value
            x = instance.__dict__['_RectOfVirus'].x
            instance.__dict__['_RectOfVirus'] = instance.__dict__[self._name].get_rect()
            instance.__dict__['_RectOfVirus'].bottom = 0
            instance.__dict__['_RectOfVirus'].x = x
        else:
            instance.__dict__[self._name] = value

class Virus(Sprite):
    def __init__(self, screen:pygame.Surface, virus_image, pos_x:int):
        super().__init__()
        self._screen = screen
        self._ImageOfVirus = pygame.transform.smoothscale(pygame.image.load(virus_image),  Settings().virus_size)
        self._RectOfVirus = self._ImageOfVirus.get_rect()
        self._virus_speed = Settings().virus_speed
        self._dead = False #标志着病毒的死亡

        #确定病毒位置
        self._RectOfVirus.bottom = 30
        self._RectOfVirus.x = pos_x

    ImageOfVirus = VirusProperty('ImageOfVirus')
    virus_speed = VirusProperty('virus_speed')
    dead = VirusProperty('dead')

    def blit_virus(self):
        """
        绘制病毒
        :return: None
        """
        self._screen.blit(self._ImageOfVirus, self._RectOfVirus)

    def update(self, *args):
        """
        更新病毒位置
        :param args:
        :return: None
        """
        pass
        # if self._RectOfVirus.x

# class SmallVirus(Virus):
#     def __init__(self):
#         super().__init__()
#
# class MiddleVirus(Virus):
#     def __init__(self):
#         super().__init__()
#
# class BigVirus(Virus):
#     def __init__(self):
#         super().__init__()




if __name__ == '__main__':
    pass