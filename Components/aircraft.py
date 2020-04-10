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
from MainingOperation.basic_settings import Settings
class AircraftProperty:
    def __init__(self, name):
        self._name = '_' + name
    def __get__(self, instance, owner):
        return instance.__dict__[self._name]
    def __set__(self, instance, value):
        if self._name == '_ImageOfAircraft':
            instance.__dict__[self._name] = pygame.image.load(value) if type(value) == str else value
            instance.__dict__['_rect'] = instance.__dict__[self._name].get_rect()
            instance.__dict__['_rect'].centerx = int(instance.__dict__['_screen'].get_rect().centerx / 2 \
                                                 - Settings().boundary_pos / 2)
            instance.__dict__['_rect'].bottom = instance.__dict__['_screen'].get_rect().bottom
        elif self._name == '_screen':
            instance.__dict__[self._name] = value
            instance.__dict__['_RectBorderOfScreen'] = instance.__dict__[self._name].get_rect()
            instance.__dict__['_rect'].centerx = int(instance.__dict__['_RectBorderOfScreen'].centerx / 2 \
                                                     - Settings().boundary_pos / 2)
            instance.__dict__['_rect'].bottom = instance.__dict__['_RectBorderOfScreen'].bottom
        elif self._name == '_rect':
            instance.__dict__[self._name].centerx = value[0]
            instance.__dict__[self._name].centery = value[-1]
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
        self._v = 30 #飞船速度
        #飞行器原始大小
        self._region_width = self._rect.width
        self._region_height = self._rect.height

        self._rect.centerx = int(self._RectBorderOfScreen.left +
                                 (self._RectBorderOfScreen.width - Settings().boundary_pos) / 2) #飞行器矩形框中心位置横标与屏幕矩形框中心位置横标相等
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

    def change_size(self, pos: tuple, size: tuple):
        """
        原地改变飞行器的尺寸
        :param pos: 飞行器原始位置
        :param size: 飞行器新尺寸
        :return: None
        """
        self._ImageOfAircraft = pygame.transform.smoothscale(self._ImageOfAircraft, size)
        self._rect = self._ImageOfAircraft.get_rect()
        self.rect = pos

    def reset(self):
        """
        飞船状态，大小，位置
        :return:
        """
        self._rect.centerx = int(self._RectBorderOfScreen.left + (self._RectBorderOfScreen.width - Settings().boundary_pos) / 2)  # 飞行器矩形框中心位置横标与屏幕矩形框中心位置横标相等
        self._rect.bottom = self._RectBorderOfScreen.bottom  # 飞行器矩形框底端与屏幕矩形框底端相等
        self.change_size(pos=(self._rect.centerx, self._rect.centery),
                                               size=(self._region_width, self._region_height))


if __name__ == '__main__':
    import sys
    pygame.init()
    screen = pygame.display.set_mode(size=(1200, 800))
    # screen.fill((100, 100, 100))
    aircraft = Aircraft(screen=screen)
    print(aircraft.rect)
    aircraft.ImageOfAircraft = pygame.transform.smoothscale(aircraft.ImageOfAircraft, (int(aircraft.rect.width/2), int(aircraft.rect.height/2)))
    print(type(aircraft.rect.x))
    # aircraft.rect.centerx += 1
    # for i in aircraft.rect.__dir__():
    #     print(i)
    # print(aircraft.rect.top, aircraft.RectBorderOfScreen.top)
    # print(aircraft.rect.bottom, aircraft.RectBorderOfScreen.bottom, aircraft.rect.height)
    # aircraft.ImageOfAircraft = '/Users/songyunlong/Desktop/c++程序设计实践课/病毒1.jpeg'
    # aircraft.screen = pygame.display.set_mode(size=(1000, 500))

    # while True:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             sys.exit()
    #     aircraft.blitAircraft()
    #     pygame.display.flip()