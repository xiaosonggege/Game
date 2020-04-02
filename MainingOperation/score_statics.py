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
        self._virus1_score = virus1_num #* Score.score_per_virus['level1']
        self._virus2_score = virus2_num #* Score.score_per_virus['level2']
        self._virus3_score = virus3_num #* Score.score_per_virus['level3']
        self._db = pymysql.connect('localhost', 'root', 'xiaosonggege1025', 'Game')
        self._cursor = self._db.cursor()

    name = ScoreProperty('name')
    virus1 = ScoreProperty('virus1_score')
    virus2 = ScoreProperty('virus2_score')
    virus3 = ScoreProperty('virus3_score')

    def _insert_data(self):
        self._cursor.execute('show tables')
        if self._name not in (table[0] for table in self._cursor.fetchall()):
            try:
                # 默认开启手动提交
                sql1 = """
                    create table if not exists %s (
                    name varchar(20) primary key not null ,
                    virus1 int,
                    virus2 int,
                    virus3 int,
                    score int 
                    )
                    """ % self._name
                self._cursor.execute(sql1)
            except:
                print('建表有问题')
            else:
                self._db.commit()


    def _update_table(self):
        try:
            sql1 = 'insert into zhangsan values (%s, %s, %s, %s)' % \
                   (self._name, self._virus1_score, self._virus2_score, self._virus3_score)
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

    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_val, exc_tb):
        return True







if __name__ == '__main__':
    pass