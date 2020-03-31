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



if __name__ == '__main__':
    pass