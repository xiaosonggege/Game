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

# cursor.execute("""insert into user values (4, 'd', %s)""" % a)
# cursor.execute("update user set name = 'd' where id = 3")
# cursor.execute("delete from user where id = %s" % 3)
# db.commit()
# cursor.execute('show tables')
# cursor.execute('select count(*) from user')
sql0 = 'select virus1_total, virus2_total, virus3_total from %s' % 'usr_info'
sql1 = 'describe usr_info'
cursor.execute(sql0)
db.commit()
str1 = [' '.join([str(e) for e in i]) for i in cursor.fetchall()]
print(str1)
# print(cursor.fetchall())
# cursor.execute("select max_score from usr_info where name='song'")
# print(cursor.fetchone()[0])
db.close()