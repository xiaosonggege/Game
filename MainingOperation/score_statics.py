#!/usr/bin/env python
# encoding: utf-8
'''
@author: songyunlong
@license: (C) Copyright 2020-2025.
@contact: 1243049371@qq.com
@software: pycharm
@file: score_statics
@time: 2020/3/31 11:34 上午
'''
import pymysql
import pygame
from MainingOperation.basic_settings import Settings


class ScoreProperty:
    def __init__(self, name):
        self._name = '_' + name
    def __get__(self, instance, owner):
        return instance.__dict__[self._name]
    def __set__(self, instance, value):
        instance.__dict__[self._name] = value

class Score:
    score_per_virus = {'level1':1, 'level2':3, 'level3':5}
    def __init__(self, name:str, virus1_num:int=0, virus2_num:int=0, virus3_num:int=0):
        self._name = name
        self._virus1 = virus1_num
        self._virus2 = virus2_num
        self._virus3 = virus3_num
        self._db = pymysql.connect('localhost', 'root', 'xiaosonggege1025', 'Game')
        self._cursor = self._db.cursor()
        self._score = self._virus1 * Score.score_per_virus['level1'] + \
                      self._virus2 * Score.score_per_virus['level2'] + \
                      self._virus3 * Score.score_per_virus['level3']

    name = ScoreProperty('name')
    virus1 = ScoreProperty('virus1')
    virus2 = ScoreProperty('virus2')
    virus3 = ScoreProperty('virus3')

    def scoring(self):
        self._score = self._virus1 * Score.score_per_virus['level1'] + \
                      self._virus2 * Score.score_per_virus['level2'] + \
                      self._virus3 * Score.score_per_virus['level3']

    def closing_database(self):
        self._db.close()

    def _create_usrname_table(self):
        """
        建立usr_info数据表，如果存在的话就忽略
        :return: None
        """
        self._cursor.execute('show tables')
        if 'usr_info' not in (table[0] for table in self._cursor.fetchall()):
            try:
                #默认开启手动提交
                sql1 = """
                    create table if not exists usr_info (
                    name varchar(20) primary key not null ,
                    virus1_total int not null ,
                    virus2_total int not null ,
                    virus3_total int not null ,
                    max_score int not null ,
                    index name (name)
                    )
                    """
                self._cursor.execute(sql1)
            except:
                print('建立usr_info有问题')
            else:
                self._db.commit()

    def update_usr_info(self):
        """
        更新usr_info表
        :return: None
        """
        sql0 = "insert into usr_info values ('%s', %s, %s, %s, %s)" % \
               (self._name, self._virus1, self._virus2, self._virus3, self._score)
        sql1 = "update  usr_info set virus1_total = \
        usr_info.virus1_total + %s where name = '%s'" % (self._virus1, self._name)
        sql2 = "update usr_info set virus2_total = \
        usr_info.virus2_total + %s where name = '%s'" % (self._virus2, self._name)
        sql3 = "update usr_info set virus3_total = \
        usr_info.virus3_total + %s where name = '%s'" % (self._virus3, self._name)
        sql4 = 'update usr_info set max_score = \
        (select b.a from (select max(score) as a from %s) b)' % self._name
        # self._cursor.execute('select name from usr_info')
        # if self._name not in [i[0] for i in self._cursor.fetchall()]:
        #     self._cursor.execute(sql0)
        # else:
        #     for sql in [sql1, sql2, sql3, sql4]:
        #         self._cursor.execute(sql)
        # self._db.commit()
        try:
            self._cursor.execute('select name from usr_info')
            if self._name not in [i[0] for i in self._cursor.fetchall()]:
                self._cursor.execute(sql0)
            else:
                for sql in [sql1, sql2, sql3, sql4]:
                    self._cursor.execute(sql)
        except:
            print('usr_info数据表更新出错!')
        else:
            self._db.commit()

    def create_data(self):
        self._cursor.execute('show tables')
        if self._name not in (table[0] for table in self._cursor.fetchall()):
            try:
                # 默认开启手动提交
                sql1 = """
                    create table if not exists %s (
                    virus1 int default 0,
                    virus2 int default 0,
                    virus3 int default 0,
                    score int default 0
                    )
                    """ % self._name
                self._cursor.execute(sql1)
            except:
                print('建表有问题')
            else:
                self._db.commit()


    def update_table(self):
        #计算总分

        try:
            sql1 = 'insert into %s values (%s, %s, %s, %s)' % \
                   (self._name, self._virus1, self._virus2, self._virus3, self._score)
            self._cursor.execute(sql1)
            sql2 = 'select count(*) from %s' % self._name
            self._cursor.execute(sql2)

            #如果成绩表中成绩多余10项，就删除最差成绩，使表中数据始终为10项
            if self._cursor.fetchone()[0] > 10:
                sql3 = 'delete from %s where score = (select a.b from (select min(score) as b from %s) a)' %\
                       (self._name, self._name)
                self._cursor.execute(sql3)
        except:
            print('更新表有问题')
        else:
            # 加入统计信息：最高分前几个，排序等等
            self._db.commit()

    def total_virus(self):
        """
        总共消灭病毒数
        :return: the number of virus
        """
        try:
            sql = 'select sum(virus1)+sum(virus2)+sum(virus3) as sum from %s' % self._name
            self._cursor.execute(sql)
        except:
            print('查询有问题')
        else:
            self._db.commit()
            return self._cursor.fetchone()[0]

    def outprint(self, name):
        """
        输出数据
        :param name: 用户名
        :return:
        """
        #usrname
        usrname = 'usrname: %s' % name

        #历史最高分
        sql0 = "select max_score from usr_info where name='%s'" % name
        self._cursor.execute(sql0)
        maxscore = 'max score: %s' % self._cursor.fetchone()[0]

        #十次最好成绩属性
        sql1 = 'describe %s' % name
        self._cursor.execute(sql1)
        # column_name = ' '.join([e[0] for e in self._cursor.fetchall()])
        column_name = '{0:8} {1:8} {2:8} {3:8}'.format(*[e[0] for e in self._cursor.fetchall()])
        sql2 = 'select * from %s' % name
        self._cursor.execute(sql2)
        content = ['{0:8}    {1:8}    {2:8}    {3:8}'.format(*[str(e) for e in i]) for i in self._cursor.fetchall()]
        #所有内容组成列表输出
        content.insert(0, usrname)
        content.insert(1, maxscore)
        content.insert(2, column_name)
        return content

    def __enter__(self):
        self._create_usrname_table()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return True

class ScoreBoarder:
    def __init__(self, screen:pygame.Surface, width:int=150,
                 height:int=50, button_color=Settings().bg_color,
                 text_color=(255, 255, 255), text_size=38):
        self._screen = screen
        self._RectOfScreen = self._screen.get_rect()
        #设置按钮
        self._width = width
        self._height = height
        self._button_color = button_color
        self._text_color = text_color
        self._font = pygame.font.SysFont(name=None, size=text_size)
        self.rect = pygame.Rect(0, 0, self._width, self._height)
        self.rect.centerx = self._RectOfScreen.right - Settings().boundary_pos / 2
        self.rect.centery = self._height + 270
        self._msg = 0

    @property
    def msg(self):
        return self._msg
    @msg.setter
    def msg(self, message:int):
        self._msg = message

    def msg_set(self):
        self._msg_image = self._font.render('score:%s' % self._msg, True, self._text_color, self._button_color)
        self._msg_image_rect = self._msg_image.get_rect()
        self._msg_image_rect.center = self.rect.center

    def draw_button(self):
        #绘制一个用颜色填充的矩形，并在矩形上绘制文本Surface
        self._screen.fill(color=self._button_color, rect=self.rect)
        self._screen.blit(self._msg_image, self._msg_image_rect)

if __name__ == '__main__':
    with Score('xing') as score:
        # score.virus1 = 2
        # score.virus2 = 2
        # score.virus3 = 3
        # score.scoring()
        # score.create_data()
        # score.update_table()
        # # print(score.total_virus())
        # score.update_usr_info()
        print(score.outprint('song'))
