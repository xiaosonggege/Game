#!/usr/bin/env python
# encoding: utf-8
'''
@author: songyunlong
@license: (C) Copyright 2020-2025.
@contact: 1243049371@qq.com
@software: pycharm
@file: aircraft
@time: 2020/3/19 5:54 下午
'''
import pygame
class AircraftProperty:
    def __init__(self, name):
        self._name = '_' + name
    def __get__(self, instance, owner):
        return instance.__dict__[self._name]
    def __set__(self, instance, value):
        if self._name == '_ImageOfAircraft':
            instance.__dict__[self._name] = pygame.image.load(value) if type(value) == str else value
            instance.__dict__['_rect'] = instance.__dict__[self._name].get_rect()
            instance.__dict__['_rect'].centerx = instance.__dict__['_screen'].get_rect().centerx
            instance.__dict__['_rect'].bottom = instance.__dict__['_screen'].get_rect().bottom
        elif self._name == '_screen':
            instance.__dict__[self._name] = value
            instance.__dict__['_RectBorderOfScreen'] = instance.__dict__[self._name].get_rect()
            instance.__dict__['_rect'].centerx = instance.__dict__['_RectBorderOfScreen'].centerx
            instance.__dict__['_rect'].bottom = instance.__dict__['_RectBorderOfScreen'].bottom
        else:
            instance.__dict__[self._name] = value

class Aircraft:
    def __init__(self, screen:pygame.Surface):
        """
        飞行器基类构造函数
        :param screen: 屏幕Surface
        """
        self._screen = screen #屏幕Surface
        self._ImageOfAircraft = pygame.image.load('/Users/songyunlong/Desktop/c++程序设计实践课/ship.bmp') #飞行器Surface
        self._RectBorderOfScreen = self._screen.get_rect() #屏幕矩形框Rect
        self._rect = self._ImageOfAircraft.get_rect() #飞行器矩形框Rect
        self._v = 1.5 #飞船速度

        self._rect.centerx = self._RectBorderOfScreen.centerx #飞行器矩形框中心位置横标与屏幕矩形框中心位置横标相等
        self._rect.bottom = self._RectBorderOfScreen.bottom #飞行器矩形框底端与屏幕矩形框底端相等
    screen = AircraftProperty('screen')
    ImageOfAircraft = AircraftProperty('ImageOfAircraft')
    rect = AircraftProperty('rect')
    v = AircraftProperty('v')
    RectBorderOfScreen = AircraftProperty('RectBorderOfScreen')

    def blitAircraft(self):
        """
        将飞行器显示到屏幕上
        :return: None
        """
        self._screen.blit(self._ImageOfAircraft, self._rect)
        # print(self._rect)

if __name__ == '__main__':
    import sys
    pygame.init()
    screen = pygame.display.set_mode(size=(1200, 800))
    screen.fill((100, 100, 100))
    aircraft = Aircraft(screen=screen)
    aircraft.rect.centerx += 1
    # for i in aircraft.rect.__dir__():
    #     print(i)
    print(aircraft.rect.top, aircraft.RectBorderOfScreen.top)
    print(aircraft.rect.bottom, aircraft.RectBorderOfScreen.bottom, aircraft.rect.height)
    # aircraft.ImageOfAircraft = '/Users/songyunlong/Desktop/c++程序设计实践课/病毒1.jpeg'
    # aircraft.screen = pygame.display.set_mode(size=(1000, 500))

    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             sys.exit()
    #     aircraft.blitAircraft()
    #     pygame.display.flip()