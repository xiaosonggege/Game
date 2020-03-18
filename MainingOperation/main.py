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
class Main:
    def main(self):
        pygame.init()
        screen = pygame.display.set_mode(size=(1200, 800))
        pygame.display.set_caption("Alien Invasion")
        bg_color = (100, 100, 100)
        screen.fill(bg_color)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.flip()


if __name__ == '__main__':
    Main().main()