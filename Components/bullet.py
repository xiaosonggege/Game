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
from pygame.sprite import Sprite
from MainingOperation.basic_settings import Settings
from Components.aircraft import Aircraft
class BulletProperty:
    def __init__(self, name):
        self._name = name
    def __get__(self, instance, owner):
        return instance.__dict__[self._name]
    def __set__(self, instance, value:Settings):
        # if self._name == '_aircraft':
        #     instance.__dict__[self._name] = value
        #     instance.__dict__['_RectOfBullet'].centerx = value.rect.centerx
        #     instance.__dict__['_RectOfBullet'].top = value.rect.top
        if self._name == 'rect': #此时value为Settings实例
            instance.__dict__[self._name] = pygame.Rect(
                instance.__dict__[self._name].centerx,
                instance.__dict__[self._name].top,
                *value.bullet_size)

class Bullet(Sprite):
    def __init__(self, screen:pygame.Surface, aircraft:Aircraft):
        super().__init__()
        self._screen = screen
        self._aircraft = aircraft
        #子弹边框x, y, width, height
        self.rect = pygame.Rect(0, 0, *Settings().bullet_size)
        #子弹初始位置与飞行器位置对齐
        self.rect.centerx = self._aircraft.rect.centerx
        self.rect.top = self._aircraft.rect.top

        self._color = Settings().bullet_color #子弹颜色
        self._speed = Settings().bullet_speed #子弹速度
    rect_ = BulletProperty('rect')

    def update(self):
        """
        更新飞行器位置
        :return: None
        """
        self.rect.centery = float(self.rect.centery) - self._speed
    def draw_Bullet(self):
        """
        在screen上绘制子弹
        :return: None
        """
        pygame.draw.rect(self._screen, self._color, self.rect)

if __name__ == '__main__':
    import sys
    pygame.init()
    screen = pygame.display.set_mode(size=(1200, 800))
    screen.fill((100, 100, 100))
    aircraft = Aircraft(screen=screen)
    b = Bullet(screen=screen, aircraft=aircraft)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        b.draw_Bullet()
        pygame.display.flip()
