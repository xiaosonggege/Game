#!/usr/bin/env python
# encoding: utf-8
'''
@author: songyunlong
@license: (C) Copyright 2020-2025.
@contact: 1243049371@qq.com
@software: pycharm
@file: basic_settings
@time: 2020/3/18 7:49 下午
'''
import pygame
class SettingsProperty:
    def __init__(self, name):
        self._name = '_' + name
    def __get__(self, instance, owner):
        return instance.__dict__[self._name]
    def __set__(self, instance, value):
        if type(value) is not str: #不传入背景图片路径(背景使用纯色)
            instance.__dict__[self._name] = value
        else: #使用自定义传入的背景图片
            instance.__dict__[self._name] = pygame.image.load(value)

class Settings:
    def __init__(self, background_path=None):
        self._screen_width = 1200
        self._screen_height = 800
        self._bg_color = (230, 230, 230) if not background_path else None
        self._background = pygame.image.load(background_path) if background_path is not None else None
    screen_width = SettingsProperty('screen_width')
    screen_height = SettingsProperty('screen_height')
    bg_color = SettingsProperty('bg_color')
    background = SettingsProperty('background')

if __name__ == '__main__':
    s = Settings()
    print(s.screen_height, s.screen_width, s.bg_color, s.background)
    s.bg_color = (2, 3, 4)
    print(s.screen_height, s.screen_width, s.bg_color, s.background)
