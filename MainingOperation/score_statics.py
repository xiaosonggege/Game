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
        self._virus1 = virus1_num #* Score.score_per_virus['level1']
        self._virus2 = virus2_num #* Score.score_per_virus['level2']
        self._virus3 = virus3_num #* Score.score_per_virus['level3']
        self._db = pymysql.connect('localhost', 'root', 'xiaosonggege1025', 'Game')
        self._cursor = self._db.cursor()

    name = ScoreProperty('name')
    virus1 = ScoreProperty('virus1_score')
    virus2 = ScoreProperty('virus2_score')
    virus3 = ScoreProperty('virus3_score')

    def _create_usrname_table(self):
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
                    index name (name)
                    )
                    """
                self._cursor.execute(sql1)
            except:
                print('建立usr_info有问题')
            else:
                self._db.commit()

    def create_data(self):
        self._cursor.execute('show tables')
        if self._name not in (table[0] for table in self._cursor.fetchall()):
            try:
                # 默认开启手动提交
                sql1 = """
                    create table if not exists %s (
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


    def update_table(self):
        #计算总分
        self._score = self._virus1 * Score.score_per_virus['level1'] + \
                      self._virus2 * Score.score_per_virus['level2'] + \
                      self._virus3 * Score.score_per_virus['level3']
        try:
            sql1 = 'insert into %s values (%s, %s, %s, %s)' % \
                   (self._name, self._virus1, self._virus2, self._virus3, self._score)
            print('1')
            self._cursor.execute(sql1)
            print('no pa1')
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

    def storage_total_viruses(self, usrname:str):
        """
        存储并更新不同玩家所击杀的总病毒数量
        :param usrname: 玩家姓名
        :return: None
        """
        sql1 =


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
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        return True


if __name__ == '__main__':
    score = Score('song', 2, 2, 2)
    score.create_data()
    # score.update_table()
    print(score.total_virus())