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

class VirusProperty:
    def __init__(self, name):
        self._name = name
    def __get__(self, instance, owner):
        return instance.__dict__[self._name]
    def __set__(self, instance, value):
        if self._name == '_ImageOfVirus':
            instance.__dict__[self._name] = value
            x = instance.__dict__['rect'].x
            instance.__dict__['rect'] = instance.__dict__[self._name].get_rect()
            instance.__dict__['rect'].bottom = 0
            instance.__dict__['rect'].x = x
        else:
            instance.__dict__[self._name] = value

class Virus(Sprite):
    def __init__(self, screen:pygame.Surface, virus_image, pos_x:int):
        super().__init__()
        self._screen = screen
        self._ImageOfVirus = pygame.transform.smoothscale(pygame.image.load(virus_image),  Settings().virus_size)
        self.rect = self._ImageOfVirus.get_rect()
        self._virus_speed = Settings().virus_speed
        self._dead = False #标志着病毒的死亡
        #确定病毒位置
        self.rect.bottom = 30
        self.rect.right = pos_x

    ImageOfVirus = VirusProperty('_ImageOfVirus')
    virus_speed = VirusProperty('_virus_speed')
    dead = VirusProperty('_dead')

    def blit_virus(self):
        """
        绘制病毒
        :return: None
        """
        self._screen.blit(self._ImageOfVirus, self.rect)

    def update(self, *args):
        """
        更新病毒位置
        :param args:
        :return: None
        """
        position_x = np.random.choice(a=[-1, 1], p=[0.5, 0.5])
        if position_x == -1:
            if self.rect.left >= 0:
                if self.rect.left - self._virus_speed > 0:
                    self.rect.left -= self._virus_speed
                else:
                    self.rect.left = 0
            else:
                self.rect.left += self._virus_speed
        else:
            if self.rect.right <= self._screen.get_rect().right - Settings().boundary_pos:
                if self.rect.right + self._virus_speed < self._screen.get_rect().right - Settings().boundary_pos:
                    self.rect.right += self._virus_speed
                else:
                    self.rect.right = self._screen.get_rect().right - Settings().boundary_pos
            else:
                self.rect.right -= self._virus_speed
        self.rect.y += self._virus_speed

class VirusStyle2(Virus):
    """
    能分裂的病毒，每个病毒有0.5的概率分裂成两个病毒
    """
    def __init__(self, screen:pygame.Surface, virus_image, pos_x:int):
        super().__init__(screen=screen, virus_image=virus_image, pos_x=pos_x)

#
# class VirusStyle3(Virus):
#     def __init__(self):
#         super().__init__()
#
# class BigVirus(Virus):
#     def __init__(self):
#         super().__init__()




if __name__ == '__main__':
    pass