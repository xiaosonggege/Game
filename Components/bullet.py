#!/usr/bin/env python
# encoding: utf-8
'''
@author: songyunlong
@license: (C) Copyright 2020-2025.
@contact: 1243049371@qq.com
@software: pycharm
@file: Bullet
@time: 2020/3/22 11:56 下午
'''
import pygame
from pygame.sprite import Sprite, Group

class Bullet(Sprite):
    def __init__(self, screen, aircraft):
        super().__init__()
        self._screen = screen
        #子弹边框x, y, width, height
        self._RectOfBullet = pygame.Rect(0, 0, 5, 10)
        #子弹初始位置与飞行器位置对齐
        self._RectOfBullet.centerx = aircraft.rect.centerx
        self._RectOfBullet.top = aircraft.rect.top



if __name__ == '__main__':
    pass