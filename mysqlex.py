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
                     'xiaosonggege1025', 'MyfirstDatabase')
cursor = db.cursor()
a = 700
# cursor.execute("""insert into user values (4, 'd', %s)""" % a)
# cursor.execute("update user set name = 'd' where id = 3")
# cursor.execute("delete from user where id = %s" % 3)
# db.commit()
print(cursor.execute('describe user'))
# cursor.execute('select * from user')
for i in cursor.fetchall():
    print(i[2])
# print(cursor.fetchall().__class__)
db.close()