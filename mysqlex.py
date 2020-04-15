#!/usr/bin/env python
# encoding: utf-8
'''
@author: songyunlong
@license: (C) Copyright 2020-2025.
@contact: 1243049371@qq.com
@software: pycharm
@file: mysqlex
@time: 2020/3/21 3:18 下午
'''
import pymysql

db = pymysql.connect('localhost', 'root',
                     'xiaosonggege1025', 'Game')
cursor = db.cursor()
sql = 'show tables'
cursor.execute(sql)
a = 'liu' in [i[0] for i in cursor.fetchall()]
print(a)
db.commit()
db.close()