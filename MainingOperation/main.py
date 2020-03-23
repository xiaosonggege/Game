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
from Components.bullet import Bullet
from pygame.sprite import Group, Sprite
class Main:

    def __init__(self):
        self._screen = pygame.display.set_mode(size=(1200, 800))
        self._aircraft = Aircraft(self._screen)
        self._bullets = Group() #创建存储子弹的编组
        #原尺寸
        self._size_original = (self._aircraft.rect.width, self._aircraft.rect.height)
        #缩小尺寸
        self._size_small = (int(self._aircraft.rect.width/2), int(self._aircraft.rect.height/2))
        #变大尺寸1
        self._size_big1 = (self._aircraft.rect.width*2, self._aircraft.rect.height*2)
        #变大尺寸2
        self._size_big2 = (self._aircraft.rect.width*3, self._aircraft.rect.height*3)
        self._can_up = True
        self._can_down = True
        self._can_left = True
        self._can_right = True
        self._can_back = False

    def _event_checking(self):
        """
        事件队列检查
        :return: None
        """
        keys_pressed = pygame.key.get_pressed()
        #对飞行器
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
            self._aircraft.change_size(pos=(self._aircraft.rect.centerx, self._aircraft.rect.centery),
                                       size=self._size_big1)
        if keys_pressed[pygame.K_3]:
            self._aircraft.change_size(pos=(self._aircraft.rect.centerx, self._aircraft.rect.centery),
                                       size=self._size_big2)
        if keys_pressed[pygame.K_1]:
            if not self._can_back:
                self._aircraft.change_size(pos=(self._aircraft.rect.centerx, self._aircraft.rect.centery),
                                           size=self._size_small)
                self._can_back = True
            else:
                self._aircraft.change_size(pos=(self._aircraft.rect.centerx, self._aircraft.rect.centery),
                                           size=self._size_original)
                self._can_back = False

        #对子弹
        if keys_pressed[pygame.K_SPACE]:
            new_bullet = Bullet(screen=self._screen, aircraft=self._aircraft)
            self._bullets.add(new_bullet)#将新子弹加入编组进行管理

        #退出键
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
        #更新所有子弹
        self._bullets.update()
        if self._can_up and self._aircraft.rect.top >= self._aircraft.RectBorderOfScreen.top:
            if self._aircraft.rect.top - self._aircraft.RectBorderOfScreen.top <= self._aircraft.v:
                self._aircraft.rect.top = self._aircraft.RectBorderOfScreen.top
            else:
                pre_pos = float(self._aircraft.rect.centery)
                self._aircraft.rect.centery = pre_pos - self._aircraft.v
        elif self._aircraft.rect.top < self._aircraft.RectBorderOfScreen.top: #控制飞行器大小切换后机身不出边界
            self._aircraft.rect.top = self._aircraft.RectBorderOfScreen.top

        if self._can_down and self._aircraft.rect.bottom <= self._aircraft.RectBorderOfScreen.bottom:
            if self._aircraft.RectBorderOfScreen.bottom - self._aircraft.rect.bottom <= self._aircraft.v:
                self._aircraft.rect.bottom = self._aircraft.RectBorderOfScreen.bottom
            else:
                pre_pos = float(self._aircraft.rect.centery)
                self._aircraft.rect.centery = pre_pos + self._aircraft.v
        elif self._aircraft.rect.bottom > self._aircraft.RectBorderOfScreen.bottom: #同上
            self._aircraft.rect.bottom = self._aircraft.RectBorderOfScreen.bottom

        if self._can_left and self._aircraft.rect.left >= self._aircraft.RectBorderOfScreen.left:
            if self._aircraft.rect.left - self._aircraft.RectBorderOfScreen.left <= self._aircraft.v:
                self._aircraft.rect.left = self._aircraft.RectBorderOfScreen.left
            else:
                pre_pos = float(self._aircraft.rect.centerx)
                self._aircraft.rect.centerx = pre_pos - self._aircraft.v
        elif self._aircraft.rect.left < self._aircraft.RectBorderOfScreen.left: #同上
            self._aircraft.rect.left = self._aircraft.RectBorderOfScreen.left

        if self._can_right and self._aircraft.rect.right <= self._aircraft.RectBorderOfScreen.right:
            if self._aircraft.RectBorderOfScreen.right - self._aircraft.rect.right <= self._aircraft.v:
                self._aircraft.rect.right = self._aircraft.RectBorderOfScreen.right
            else:
                pre_pos = float(self._aircraft.rect.centerx)
                self._aircraft.rect.centerx = pre_pos + self._aircraft.v
        elif self._aircraft.rect.right > self._aircraft.RectBorderOfScreen.right:
            self._aircraft.rect.right = self._aircraft.RectBorderOfScreen.right

        self._aircraft.blitAircraft()
        # 在飞船和外星人后面重绘所有子弹
        for bullet in self._bullets.sprites():  # 返回编组中的所有精灵的列表
            bullet.draw_Bullet()
        #删除消失的子弹
        for bullet in self._bullets.sprites():
            if bullet.RectOfBullet.bottom < 0:
                self._bullets.remove(bullet)

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