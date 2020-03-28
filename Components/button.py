#!/usr/bin/env python
# encoding: utf-8
'''
@author: songyunlong
@license: (C) Copyright 2020-2025.
@contact: 1243049371@qq.com
@software: pycharm
@file: button
@time: 2020/3/28 6:13 下午
'''
import pygame

class Button:
    def __init__(self, screen:pygame.Surface, message:str):
        self._screen = screen
        self._RectOfScreen = self._screen.get_rect()
        #设置按钮
        self._width, self._height = 100, 50
        self._button_color = (255, 0, 0)
        self._text_color = (255, 255, 255)
        #None为使用pygame的默认字体
        self._font = pygame.font.SysFont(name=None, size=48) #从系统字体库创建一个 Font 对象
        #将按钮放在屏幕中央
        self.rect = pygame.Rect(0, 0, self._width, self._height)
        self.rect.center = self._RectOfScreen.center
        #文本Surface
        self._prep_msg = self._msg_set(msg=message)

    def _msg_set(self, msg:str):
        #创建一个新的 Surface 对象，并在上边渲染指定的文本。
        self._msg_image = self._font.render(msg, True, self._text_color, self._button_color)
        self._msg_image_rect = self._msg_image.get_rect()
        self._msg_image_rect.center = self._RectOfScreen.center

    def draw_button(self):
        #绘制一个用颜色填充的按钮，再绘制文本
        self._screen.fill(color=self._button_color, rect=self.rect) #按钮在屏幕中央着色
        self._screen.blit(self._msg_image, self._msg_image_rect) #按钮绘制在屏幕中央

if __name__ == '__main__':
    pass