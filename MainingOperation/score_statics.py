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

class Score:
    score_per_virus = {'level1':1, 'level2':3, 'level3':5}
    def __init__(self, name:str, virus1_num:int=0, virus2_num:int=0, virus3_num:int=0):
        self._name = name
        self._virus1_score = Score.score_per_virus['level1'] * virus1_num
        self._virus2_score = Score.score_per_virus['level2'] * virus2_num
        self._virus3_score = Score.score_per_virus['level3'] * virus3_num
        self._db = pymysql.connect('localhost', 'root', 'xiaosonggege1025', 'Game')
        self._cursor = self._db.cursor()

    def _create(self):
        self._cursor.execute('show tables')
        if self._name not in (table[0] for table in self._cursor.fetchall()):
            #默认开启手动提交
            sql1 = """
                  create table if not exists %s (
                  name varchar(20) primary key not null ,
                  virus1 int,
                  virus2 int,
                  virus3 int
                  )
                  """ % self._name
            self._cursor.execute(sql1)
        sql2 = 'insert into zhangsan values (%s, %s, %s, %s)' % \
                (self._name, self._virus1_score, self._virus2_score, self._virus3_score)
        self._cursor.execute(sql2)
        #加入统计信息：最高分前几个，排序等等
        self._db.commit()





if __name__ == '__main__':
    pass