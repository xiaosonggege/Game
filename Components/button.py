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
from MainingOperation.basic_settings import Settings
class StartButton:
    def __init__(self, screen:pygame.Surface, message:str,
                 width:int=100, height:int=50, button_color=(255, 0, 0),
                 text_color=(255, 255, 255), text_size=48, pos=None):
        self._screen = screen
        self._RectOfScreen = self._screen.get_rect()
        #设置按钮
        self._width, self._height = width, height
        self._button_color = button_color
        self._text_color = text_color
        #None为使用pygame的默认字体
        self._font = pygame.font.SysFont(name=None, size=text_size) #从系统字体库创建一个 Font 对象
        #防止按钮
        self.rect = pygame.Rect(0, 0, self._width, self._height)
        self.rect.centerx = self._RectOfScreen.right - Settings().boundary_pos / 2 if pos is None else self._RectOfScreen.centerx
        self.rect.centery = self._height + 50 if pos is None else self._RectOfScreen.centery
        #文本Surface
        self._prep_msg = self._msg_set(msg=message)

    @property
    def width_height(self):
        return self._width, self._height
    @width_height.setter
    def width_height(self, value:tuple):
        self._width, self._height = value

    def _msg_set(self, msg:str):
        #创建一个新的 Surface 对象，并在上边渲染指定的文本。
        self._msg_image = self._font.render(msg, True, self._text_color, self._button_color)
        self._msg_image_rect = self._msg_image.get_rect()
        self._msg_image_rect.center = self.rect.center

    def draw_button(self):
        #绘制一个用颜色填充的按钮，再绘制文本
        self._screen.fill(color=self._button_color, rect=self.rect) #按钮着色
        self._screen.blit(self._msg_image, self._msg_image_rect) #按钮绘制

class LevelButton(StartButton):
    def __init__(self, screen:pygame.Surface, message:str):
        super().__init__(screen=screen, message=message, width=100, height=50)
        self._width = int(super().width_height[0] / 5)
        self._height = super().width_height[-1]
        # 均匀摆放等级按钮
        self.rect = pygame.Rect(0, 0, self._width, self._height)
        self.rect.centerx = int(self._RectOfScreen.right + Settings().boundary_pos * (int(message) * 0.25 - 1)) # (int(message)-1) * 2 * self._width
        self.rect.centery = self._height + 130
        self._prep_msg = super()._msg_set(msg=message)
        self._is_pressed = False

    @property
    def pressed(self):
        return self._is_pressed
    @pressed.setter
    def pressed(self, value:bool=True):
        self._is_pressed = True

    def draw_button(self):
        self._screen.fill(color=self._button_color, rect=self.rect) #按钮着色
        if not self._is_pressed: # 按钮按下后文本消失
            self._screen.blit(self._msg_image, self._msg_image_rect)

class Username:
    def __init__(self, screen:pygame.Surface, message:str='username'):
        self._username = message
        self._screen = screen
        self._RectOfScreen = self._screen.get_rect()
        #设置输入框大小
        self._width, self._height = 100, 50
        self._background_color = (255, 0, 0)
        self._text_color = (0, 255, 0)
        #字体
        self._font = pygame.font.SysFont(name=None, size=48)
        self.rect = pygame.Rect(0, 0, self._width, self._height)
        self.rect.centerx = self._RectOfScreen.right - Settings().boundary_pos / 2
        self.rect.centery = 600
        #文本surface
        self._prep_msg = self._msg_set(msg=self._username)

    def _msg_set(self, msg:str):
        self._msg_image = self._font.render(msg, True, self._text_color, self._background_color)
        self._msg_image_rect = self._msg_image.get_rect()
        self._msg_image_rect.center = self.rect.center

    def draw_button(self):
        #绘制一个用颜色填充的按钮，再绘制文本
        self._screen.fill(color=self._background_color, rect=self.rect) #按钮着色
        self._screen.blit(self._msg_image, self._msg_image_rect) #按钮绘制

    def text_change(self, added_word:str=None, is_delete:bool=False):
        """
        时刻根据用户输入改变Surface中的文本信息
        :return:
        """
        if is_delete:
            self._username = self._username[:-1]
            self._prep_msg = self._msg_set(msg=self._username)
        elif added_word is not None:
            self._username = self._username + added_word
            self._prep_msg = self._msg_set(msg=self._username)

    def input_event_checking(self, keys_pressed):
        """
        检测按键，并根据按键输出
        :param keys_pressed:
        :return:
        """
        if keys_pressed[pygame.K_a]:
            return 'a'
        elif keys_pressed[pygame.K_b]:
            return 'b'
        elif keys_pressed[pygame.K_c]:
            return 'c'
        elif keys_pressed[pygame.K_d]:
            return 'd'
        elif keys_pressed[pygame.K_e]:
            return 'e'
        elif keys_pressed[pygame.K_f]:
            return 'f'
        elif keys_pressed[pygame.K_g]:
            return 'g'
        elif keys_pressed[pygame.K_h]:
            return 'h'
        elif keys_pressed[pygame.K_i]:
            return 'i'
        elif keys_pressed[pygame.K_j]:
            return 'j'
        elif keys_pressed[pygame.K_k]:
            return 'k'
        elif keys_pressed[pygame.K_l]:
            return 'l'
        elif keys_pressed[pygame.K_m]:
            return 'm'
        elif keys_pressed[pygame.K_n]:
            return 'n'
        elif keys_pressed[pygame.K_o]:
            return 'o'
        elif keys_pressed[pygame.K_p]:
            return 'p'
        elif keys_pressed[pygame.K_q]:
            return 'q'
        elif keys_pressed[pygame.K_r]:
            return 'r'
        elif keys_pressed[pygame.K_s]:
            return 's'
        elif keys_pressed[pygame.K_t]:
            return 't'
        elif keys_pressed[pygame.K_u]:
            return 'u'
        elif keys_pressed[pygame.K_v]:
            return 'v'
        elif keys_pressed[pygame.K_w]:
            return 'w'
        elif keys_pressed[pygame.K_x]:
            return 'x'
        elif keys_pressed[pygame.K_y]:
            return 'y'
        elif keys_pressed[pygame.K_z]:
            return 'z'
        elif keys_pressed[pygame.K_DELETE]:
            return 'delete'





if __name__ == '__main__':
    pass