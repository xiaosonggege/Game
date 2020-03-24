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
        #screen
        self._screen_width = 1200
        self._screen_height = 800
        self._bg_color = (230, 230, 230) if not background_path else None
        self._background = pygame.image.load(background_path) if background_path is not None else None
        #bullet
        self._bullet_color = 60, 60, 60
        self._bullet_size = 3, 15
        self._bullet_speed = 30
        #virus
        self._virus_size = 50, 50
        self._virus_speed = 20
    screen_width = SettingsProperty('screen_width')
    screen_height = SettingsProperty('screen_height')
    bg_color = SettingsProperty('bg_color')
    background = SettingsProperty('background')
    bullet_color = SettingsProperty('bullet_color')
    bullet_size = SettingsProperty('bullet_size')
    bullet_speed = SettingsProperty('bullet_speed')
    virus_size = SettingsProperty('virus_size')
    virus_speed = SettingsProperty('virus_speed')

#带有加速度
class PosWithAccelerate:
    def __init__(self, can_positive, can_negative, v):
        self._time = 1
        self._can_positive = can_positive
        self._can_negative = can_negative
        self._v = v

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return True

    def __iter__(self):
        return self

    def __next__(self):
        if self._can_positive and not self._can_negative:
            return self._v * self._time + 0.5 * 1 * self._v ** 2



if __name__ == '__main__':
    s = Settings()
    print(s.screen_height, s.screen_width, s.bg_color, s.background)
    s.bg_color = (2, 3, 4)
    print(s.screen_height, s.screen_width, s.bg_color, s.background)
