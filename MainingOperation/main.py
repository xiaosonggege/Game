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
        self._screen = pygame.display.set_mode(size=(1200, 800))
        self._aircraft = Aircraft(self._screen)
        self._can_up = True
        self._can_down = True
        self._can_left = True
        self._can_right = True

    def _event_checking(self):
        """
        事件队列检查
        :return: None
        """
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            self._can_right = True
        else:
            self._can_right = False
        if keys_pressed[pygame.K_LEFT]:
            self._can_left = True
        else:
            self._can_left = False
        if keys_pressed[pygame.K_UP]:
            self._can_up = True
        else:
            self._can_up = False
        if keys_pressed[pygame.K_DOWN]:
            self._can_down = True
        else:
            self._can_down = False
        if keys_pressed[pygame.K_2]:
            self._aircraft.ImageOfAircraft = pygame.transform.scale(
                self._aircraft.ImageOfAircraft, (self._aircraft.rect.width*2, self._aircraft.rect.height*2))
        if keys_pressed[pygame.K_3]:
            self._aircraft.ImageOfAircraft = pygame.transform.scale(
                self._aircraft.ImageOfAircraft, (self._aircraft.rect.width*3, self._aircraft.rect.height*3))
        if keys_pressed[pygame.K_4]:
            self._aircraft.ImageOfAircraft = pygame.transform.scale(
                self._aircraft.ImageOfAircraft, (self._aircraft.rect.width*4, self._aircraft.rect.height*4))
        if keys_pressed[pygame.K_1]:
            self._aircraft.ImageOfAircraft = pygame.transform.scale(
                self._aircraft.ImageOfAircraft, (self._aircraft.rect.width/2, self._aircraft.rect.height/2))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def _update_scene(self):
        """
        更新屏幕中的场景
        :return: None
        """
        bg_color = (100, 100, 100)
        self._screen.fill(bg_color)
        if self._can_up and self._aircraft.rect.top > self._aircraft.RectBorderOfScreen.top:
            print(self._aircraft.rect.top, self._aircraft.RectBorderOfScreen.top)
            pre_pos = float(self._aircraft.rect.centery)
            self._aircraft.rect.centery = pre_pos - self._aircraft.v
        if self._can_down and self._aircraft.rect.bottom < self._aircraft.RectBorderOfScreen.bottom:
            pre_pos = float(self._aircraft.rect.centery)
            self._aircraft.rect.centery = pre_pos + self._aircraft.v
        if self._can_left and self._aircraft.rect.left > self._aircraft.RectBorderOfScreen.left:
            pre_pos = float(self._aircraft.rect.centerx)
            self._aircraft.rect.centerx = pre_pos - self._aircraft.v
        if self._can_right and self._aircraft.rect.right < self._aircraft.RectBorderOfScreen.right:
            pre_pos = float(self._aircraft.rect.centerx)
            self._aircraft.rect.centerx = pre_pos + self._aircraft.v

        self._aircraft.blitAircraft()
        pygame.display.flip()
        # pygame.display.update()

    def main(self):
        pygame.init()
        pygame.display.set_caption("Alien Invasion")
        bg_color = (100, 100, 100)
        self._screen.fill(bg_color)
        #
        self._aircraft.v = 30
        #
        while True:
            self._event_checking()
            self._update_scene()

if __name__ == '__main__':
    Main().main()