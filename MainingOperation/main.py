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
from Components.button import StartButton, LevelButton
from pygame.sprite import Group
from Components.virus import Virus, VirusStyle2, VirusStyle3
from MainingOperation.score_statics import Score
import numpy as np

def PositionInit(low:int, high:int, count:int):
    """
    病毒数量生成器
    :param low: 下边界
    :param high: 上边界
    :param count: 病毒最大数量
    :return:
    """
    set_of_posx = np.random.randint(low=low, high=high, size=count)
    for i in set_of_posx:
        yield i

class Main:
    level_virus = {'easy':100, 'middle':300, 'defficult':500}
    #判断两条边是否有交集 返回True代表没有重叠
    have_intersection = lambda lineone, linetwo: lineone[-1] < linetwo[0] or lineone[0] > linetwo[-1]
    def __init__(self):
        #总得分
        self._total_score = 0
        #每种病毒被消灭计数
        self._virus1_num = 0
        self._virus2_num = 0
        self._virus3_num = 0
        #
        self._screen = pygame.display.set_mode(size=(Settings().screen_width, Settings().screen_height))
        self._aircraft = Aircraft(self._screen)
        self._bullets = Group() #创建存储子弹的编组
        self._viruses = Group() #创建存储病毒的编组
        self._is_win = False #标志游戏输赢
        #游戏是否开始
        self._start_playing = False
        #游戏是否暂停，游戏暂停后，所有surface都无法更新
        self._pause_playing = False

        #游戏等级
        # self._NumOfViruses = Main.level_virus['easy'] #改
        # #病毒初始位置生成器
        # self._init_posxes = PositionInit(low=self._screen.get_rect().left,
        #                                  high=self._screen.get_rect().right - Settings().boundary_pos,
        #                                  count=self._NumOfViruses) #
        #原尺寸
        self._size_original = (self._aircraft.rect.width, self._aircraft.rect.height)
        #缩小尺寸
        self._size_small = (int(self._aircraft.rect.width/2), int(self._aircraft.rect.height/2))
        #变大尺寸1
        self._size_big1 = (self._aircraft.rect.width*2, self._aircraft.rect.height*2)
        #变大尺寸2
        self._size_big2 = (self._aircraft.rect.width*3, self._aircraft.rect.height*3)
        #飞行器能否向相应方向移动的标志
        self._can_up = True
        self._can_down = True
        self._can_left = True
        self._can_right = True
        #飞行器是否处在原本大小的标志初始值
        self._is_original = True
        #飞行器是否处在第一级放大初始值
        self._is_big_level1 = False

    def _judge_state_of_aircraft(self):#改
        if self._is_original: #飞行器处于原本大小时，变大1个size
            self._aircraft.change_size(pos=(self._aircraft.rect.centerx, self._aircraft.rect.centery),
                                       size=self._size_big1)
            self._aircraft.blitAircraft()
            self._is_original = False
            self._is_big_level1 = True
        elif self._is_big_level1:
            self._aircraft.change_size(pos=(self._aircraft.rect.centerx, self._aircraft.rect.centery),
                                       size=self._size_big2)
            self._aircraft.blitAircraft()
            self._is_big_level1 = False
        elif not self._is_original and not self._is_big_level1:
            sys.exit()

    def _event_checking(self):
        """
        事件队列检查
        :return: None
        """
        #判断光标是否在按钮区域中
        def mouse_in_button_region (mouse_x, mouse_y, button):
            station1 = mouse_x >= button.rect.left
            station2 = mouse_x <= button.rect.right
            station3 = mouse_y >= button.rect.top
            station4 = mouse_y <= button.rect.bottom
            return station1 and station2 and station3 and station4

        #鼠标位置定位
        mouse_pressed = pygame.mouse.get_pressed()
        #先选游戏等级再开始游戏
        if mouse_pressed[0] == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_in_button_region(mouse_x=mouse_x, mouse_y=mouse_y, button=self._level_button1):
                self._NumOfViruses = Main.level_virus['easy']
                self._level_button1.pressed = True
            elif mouse_in_button_region(mouse_x=mouse_x, mouse_y=mouse_y, button=self._level_button2):
                self._NumOfViruses = Main.level_virus['middle']
                self._level_button2.pressed = True

            elif mouse_in_button_region(mouse_x=mouse_x, mouse_y=mouse_y, button=self._level_button3):
                self._NumOfViruses = Main.level_virus['defficult']
                self._level_button3.pressed = True

            if mouse_in_button_region(mouse_x=mouse_x, mouse_y=mouse_y, button=self._button):
                self._start_playing = True
        keys_pressed = pygame.key.get_pressed()

        # 游戏是否暂停
        if keys_pressed[pygame.K_p]:
            if not self._pause_playing:
                self._pause_playing = True
            else:
                self._pause_playing = False

        # 退出键
        if keys_pressed[pygame.K_q]:
            print('消灭病毒数量为:', self._total_score)
            print('消灭v1病毒数为{0},v2病毒数为{1},v3病毒数为{2}'.format(self._virus1_num, self._virus2_num, self._virus3_num))
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('消灭病毒数量为:', self._total_score)
                print('消灭v1病毒数为{0},v2病毒数为{1},v3病毒数为{2}'.format(self._virus1_num, self._virus2_num, self._virus3_num))
                sys.exit()
        if self._start_playing and not self._pause_playing:
            # 对飞行器
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


            # if keys_pressed[pygame.K_2]:
            #     self._aircraft.change_size(pos=(self._aircraft.rect.centerx, self._aircraft.rect.centery),
            #                                size=self._size_big1)
            # if keys_pressed[pygame.K_3]:
            #     self._aircraft.change_size(pos=(self._aircraft.rect.centerx, self._aircraft.rect.centery),
            #                                size=self._size_big2)
            if keys_pressed[pygame.K_1]:
                if not self._is_original:
                    self._aircraft.change_size(pos=(self._aircraft.rect.centerx, self._aircraft.rect.centery),
                                               size=self._size_small)
                    self._is_original = True
                else:
                    self._aircraft.change_size(pos=(self._aircraft.rect.centerx, self._aircraft.rect.centery),
                                               size=self._size_original)
                    self._is_original = False

            # 对子弹
            if keys_pressed[pygame.K_SPACE]:
                new_bullet = Bullet(screen=self._screen, aircraft=self._aircraft)
                self._bullets.add(new_bullet)  # 将新子弹加入编组进行管理
            # 如果游戏不停值或者未达到停止标志，比如赢得游戏和达到本等级病毒最大数量则病毒一直会有 测试用
            # if len(self._viruses) < self._NumOfViruses:
            #     virus_image_path = '/Users/songyunlong/Desktop/c++程序设计实践课/病毒1.jpeg'
            #     new_virus = Virus(screen=self._screen, virus_image=virus_image_path , pos_x=next(self._init_posxes)) #改
            #     self._viruses.add(new_virus)

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
        if self._start_playing and not self._pause_playing:
            # 如果游戏不停值或者未达到停止标志，比如赢得游戏和达到本等级病毒最大数量则病毒一直会有
            if len(self._viruses) <= self._NumOfViruses:  # 增加病毒数量计数，到达一定数量之后就投入新病毒
                # print(len(self._viruses))
                virus_image_path = '/Users/songyunlong/Desktop/c++程序设计实践课/病毒1.jpeg'
                # 打印病毒个数，打死的不算在内
                print(len(self._viruses))
                try:
                    # 病毒初始位置生成器
                    self._init_posxes = PositionInit(low=self._screen.get_rect().left,
                                                     high=self._screen.get_rect().right - Settings().boundary_pos,
                                                     count=self._NumOfViruses)  #
                    new_virus = Virus(screen=self._screen, virus_image=virus_image_path,
                                      pos_x=next(self._init_posxes))  # 改
                    self._viruses.add(new_virus)
                except StopIteration:
                    print('消灭病毒数量为:', self._total_score)
                    print('消灭v1病毒数为{0},v2病毒数为{1},v3病毒数为{2}'.format(self._virus1_num, self._virus2_num, self._virus3_num))
                    sys.exit()
            # 更新所有病毒
            self._viruses.update()
            # 更新所有子弹
            self._bullets.update()
            # 飞船位置更新和边界限制
            if self._can_up and self._aircraft.rect.top >= self._aircraft.RectBorderOfScreen.top:
                if self._aircraft.rect.top - self._aircraft.RectBorderOfScreen.top <= self._aircraft.v:
                    self._aircraft.rect.top = self._aircraft.RectBorderOfScreen.top
                else:
                    pre_pos = float(self._aircraft.rect.centery)
                    self._aircraft.rect.centery = pre_pos - self._aircraft.v
            elif self._aircraft.rect.top < self._aircraft.RectBorderOfScreen.top:  # 控制飞行器大小切换后机身不出边界
                self._aircraft.rect.top = self._aircraft.RectBorderOfScreen.top

            if self._can_down and self._aircraft.rect.bottom <= self._aircraft.RectBorderOfScreen.bottom:
                if self._aircraft.RectBorderOfScreen.bottom - self._aircraft.rect.bottom <= self._aircraft.v:
                    self._aircraft.rect.bottom = self._aircraft.RectBorderOfScreen.bottom
                else:
                    pre_pos = float(self._aircraft.rect.centery)
                    self._aircraft.rect.centery = pre_pos + self._aircraft.v
            elif self._aircraft.rect.bottom > self._aircraft.RectBorderOfScreen.bottom:  # 同上
                self._aircraft.rect.bottom = self._aircraft.RectBorderOfScreen.bottom

            if self._can_left and self._aircraft.rect.left >= self._aircraft.RectBorderOfScreen.left:
                if self._aircraft.rect.left - self._aircraft.RectBorderOfScreen.left <= self._aircraft.v:
                    self._aircraft.rect.left = self._aircraft.RectBorderOfScreen.left
                else:
                    pre_pos = float(self._aircraft.rect.centerx)
                    self._aircraft.rect.centerx = pre_pos - self._aircraft.v
            elif self._aircraft.rect.left < self._aircraft.RectBorderOfScreen.left:  # 同上
                self._aircraft.rect.left = self._aircraft.RectBorderOfScreen.left

            if self._can_right and self._aircraft.rect.right <= self._aircraft.RectBorderOfScreen.right \
                    - Settings().boundary_pos:
                if self._aircraft.RectBorderOfScreen.right - Settings().boundary_pos \
                        - self._aircraft.rect.right <= self._aircraft.v:
                    self._aircraft.rect.right = self._aircraft.RectBorderOfScreen.right - Settings().boundary_pos
                else:
                    pre_pos = float(self._aircraft.rect.centerx)
                    self._aircraft.rect.centerx = pre_pos + self._aircraft.v
            elif self._aircraft.rect.right > self._aircraft.RectBorderOfScreen.right - Settings().boundary_pos:
                self._aircraft.rect.right = self._aircraft.RectBorderOfScreen.right - Settings().boundary_pos

            # #飞行器，子弹和病毒应该时刻在屏幕上绘制（已放在函数体最后部分了，此处暂且注释掉）
            # self._aircraft.blitAircraft()
            # # 绘制所有病毒
            # for virus in self._viruses.sprites():
            #     virus.blit_virus()
            # # 在飞行器和病毒后面重绘所有子弹
            # for bullet in self._bullets.sprites():  # 返回编组中的所有精灵的列表
            #     bullet.draw_Bullet()
            # #
            # 击中病毒的子弹以及被击中的病毒
            collisions = pygame.sprite.groupcollide( #collisions返回当前时刻的子弹和病毒碰撞字典
                groupa=self._bullets, groupb=self._viruses, dokilla=True, dokillb=True)  # dokill是碰撞后是否立即删除
            #如果有子弹和病毒的碰撞存在
            if len(collisions.values()) > 0:
                for group_virus in list(collisions.values()):
                    for per_virus in group_virus:
                        per_virus.dead = True
                        self._total_score += per_virus.score
                        if type(per_virus) == Virus:
                            self._virus1_num += 1
                        elif type(per_virus) == VirusStyle2:
                            self._virus2_num += 1
                        else:
                            self._virus3_num += 1
                # print(list(collisions.values())[0][0].dead)
            # 删除消失的子弹
            for bullet in self._bullets.sprites():
                if bullet.rect_.bottom < 0:
                    self._bullets.remove(bullet)

            # 删除被击中且被达到击毙条件或到达屏幕底端的病毒
            for virus in self._viruses.sprites():
                if virus.rect.bottom == self._screen.get_rect().bottom:
                    self._viruses.remove(virus)
            #
            # 判断飞行器是否触碰到病毒,即飞行器变大
            for virus in self._viruses.sprites():
                # 病毒上边界与飞行器下边界y值相等且横边有交集
                if virus.rect.top == self._aircraft.rect.bottom:
                    if not Main.have_intersection((virus.rect.left, virus.rect.right),
                                                  (self._aircraft.rect.left, self._aircraft.rect.right)):
                        self._judge_state_of_aircraft()
                        # sys.exit()#改成飞行器变大,如果在变大状态下再次与病毒相撞，则退出
                # 病毒下边界与飞行器上边界y值相等且横边有交集
                if virus.rect.bottom == self._aircraft.rect.top:
                    if not Main.have_intersection((virus.rect.left, virus.rect.right),
                                                  (self._aircraft.rect.left, self._aircraft.rect.right)):
                        self._judge_state_of_aircraft()
                        # sys.exit()#改成飞行器变大
                # 病毒左边界与飞行器右边界x值相等且纵边有交集
                if virus.rect.left == self._aircraft.rect.right:
                    if not Main.have_intersection((virus.rect.top, virus.rect.bottom),
                                                  (self._aircraft.rect.top, self._aircraft.rect.bottom)):
                        self._judge_state_of_aircraft()
                        # sys.exit()#改成飞行器变大
                # 病毒有边界与飞行器左边界x值相等且纵边有交集
                if virus.rect.right == self._aircraft.rect.left:
                    if not Main.have_intersection((virus.rect.top, virus.rect.bottom),
                                                  (self._aircraft.rect.top, self._aircraft.rect.bottom)):
                        self._judge_state_of_aircraft()
                        # sys.exit()  # 改成飞行器变大

        # 飞行器，子弹和病毒应该时刻在屏幕上绘制
        if self._start_playing:
            self._aircraft.blitAircraft()
            # 绘制所有病毒
            for virus in self._viruses.sprites():
                virus.blit_virus()
            # 在飞行器和病毒后面重绘所有子弹
            for bullet in self._bullets.sprites():  # 返回编组中的所有精灵的列表
                bullet.draw_Bullet()

        #
                #
                # pygame.display.flip()
                # pygame.display.update()


    def _boundary(self):
        """
        在screen上绘制分界线，分界线右边是按钮
        :return:
        """
        line_size = 5, Settings().screen_height
        self._line = pygame.rect.Rect(0, 0, *line_size)
        self._line.centerx = self._screen.get_rect().right - Settings().boundary_pos
        self._line.centery = self._screen.get_rect().centery
        pygame.draw.rect(self._screen, (0)*3, self._line)
        # pygame.display.flip()

    def main(self):
        pygame.init()
        pygame.display.set_caption("Alien Invasion")
        bg_color = (100, 100, 100)
        self._screen.fill(bg_color)
        # 添加游戏边线
        self._boundary()
        # 按钮
        self._button = StartButton(screen=self._screen, message='play')
        self._level_button1 = LevelButton(screen=self._screen, message='1')
        self._level_button2 = LevelButton(screen=self._screen, message='2')
        self._level_button3 = LevelButton(screen=self._screen, message='3')
        #
        self._aircraft.v = 30
        #
        while True:
            # 测试用
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('消灭病毒数量为:', self._total_score)
                    print('消灭v1病毒数为{0},v2病毒数为{1},v3病毒数为{2}'.format(self._virus1_num, self._virus2_num, self._virus3_num))
                    sys.exit()

            # 添加游戏边线
            self._boundary()
            # self._button.draw_button()
            # pygame.display.flip()
            # 绘制开始按钮，在游戏未开始或者暂停时也依然在屏幕上呈现
            # if not self._start_playing:
            self._button.draw_button()
            self._level_button1.draw_button()
            self._level_button2.draw_button()
            self._level_button3.draw_button()
            pygame.display.flip()
            #游戏开始且未按下暂停键
            # if self._start_playing and not self._pause_playing:
            self._event_checking()
            self._update_scene()


if __name__ == '__main__':
    Main().main()