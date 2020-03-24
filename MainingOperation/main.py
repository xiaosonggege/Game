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
from pygame.sprite import Group
from Components.virus import Virus
class Main:
    level_virus = {'easy':100, 'middle':300, 'defficult':500}
    def __init__(self):
        self._screen = pygame.display.set_mode(size=(1200, 800))
        self._aircraft = Aircraft(self._screen)
        self._bullets = Group() #创建存储子弹的编组
        self._viruses = Group() #创建存储病毒的编组
        self._is_win = False #标志游戏输赢
        #游戏等级
        self._NumOfViruses = Main.level_virus['easy'] #改
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
        #如果游戏不停值或者未达到停止标志，比如赢得游戏和达到本等级病毒最大数量则病毒一直会有
        if len(self._viruses) < self._NumOfViruses or not self._is_win:
            new_virus = Virus(screen=self._screen, virus_image=None, pos_x=None) #改
            self._viruses.add(new_virus)
        #退出键
        if keys_pressed[pygame.K_q]:
            sys.exit()
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
        # 测试病毒类
        # virus_image_path = '/Users/songyunlong/Desktop/c++程序设计实践课/病毒1.jpeg'
        # self._virus = Virus(screen=self._screen, virus_image=virus_image_path,
        #                     pos_x=int(self._screen.get_rect().centerx))
        # self._virus.blit_virus()
        #更新所有病毒
        self._viruses.update()
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

        # 在飞行器和病毒后面重绘所有子弹
        for bullet in self._bullets.sprites():  # 返回编组中的所有精灵的列表
            bullet.draw_Bullet()
        #删除消失的子弹
        for bullet in self._bullets.sprites():
            if bullet.RectOfBullet.bottom < 0:
                self._bullets.remove(bullet)
        #删除被击中且被达到击毙条件的病毒
        for virus in self._viruses.sprites():
            if virus.dead:
                self._viruses.remove(virus)
        #
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