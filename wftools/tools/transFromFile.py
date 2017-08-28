#!/usr/bin/python
## -*- coding:utf8 -*-
import sys   
reload(sys)  
sys.setdefaultencoding('utf8')  

import json
import urllib
import MySQLdb
import types

# 打开数据库连接
db = MySQLdb.connect("localhost","root","eas140900","warframe" ,charset='utf8')

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

file = open("zh_name.txt")

def uploadDB(name,name_zh):
            # SQL 插入语句
    sql = """UPDATE item set name_zh= '%s'  where name_en = '%s' """%(name_zh,name )
    try:
       # 执行sql语句
       cursor.execute(sql)
       # 提交到数据库执行
       db.commit()
       return True
    except:
       # Rollback in case there is any error
       db.rollback()
       return False

line = file.readline()
while line:
    line = file.readline()
    l = line.split('\t')
    if(len(l)<2):
        continue
    lt = l[1].split('\n')
    l[1] = lt[0]
    if not uploadDB(l[0],l[1]):
    	print l[0]+"="+l[1]
    if not line:
        break
    pass # do something

