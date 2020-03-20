#!/usr/bin/env python
# encoding: utf-8
'''
@author: songyunlong
@license: (C) Copyright 2020-2025.
@contact: 1243049371@qq.com
@software: pycharm
@file: main
@time: 2020/3/18 8:11 下午
'''
import pygame
import sys
from MainingOperation.basic_settings import Settings
from Components.aircraft import Aircraft
class Main:
    def __init__(self):
        self._screen = pygame
        self _aircraft = Aircraft()
    def _event_checking(self):
        """
        事件队列检查
        :return: None
        """
        for event in pygame.event.get():
            if event == pygame.QUIT:
                sys.exit()
    def _update_scene(self, screen:pygame.Surface, screen_color:tuple, screen_size:tuple):
        """
        更新屏幕中的场景
        :param screen: 屏幕Surface
        :param screen_color: 屏幕背景颜色
        :param screen_size: 屏幕尺寸
        :return: None
        """
        pygame.

    def main(self):
        pygame.init()
        screen = pygame.display.set_mode(size=(1200, 800))
        pygame.display.set_caption("Alien Invasion")
        bg_color = (100, 100, 100)
        screen.fill(bg_color)
        while True:
            self._event_checking()
            pygame.display.flip()


if __name__ == '__main__':
    Main().main()