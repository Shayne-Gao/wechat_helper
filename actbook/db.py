#!/usr/bin/python
# -*- coding:utf-8 -*- 

import scrapy
import json
import urlparse
import HTMLParser
import ConfigParser
import os
import urllib
import time
import MySQLdb

class AccountBookDB:
    db = None
    cursor = None
    REC_TYPE_COST = 0
    REC_TYPE_INCOME =1
    def __init__(self):
        self.db = MySQLdb.connect("localhost","root","IWLX8IS12Rl","accountbook",charset='utf8' )
        self.cursor = self.db.cursor()

    def queryBySql(self,sql):
          # 执行SQL语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        self.db.commit()
        results = self.cursor.fetchall()
        return results

    def insertAccountRecord(self,uid,cost,type,cateid,content):
        #get item id
     
        sql = """INSERT INTO account_record (user_id,cost,type,category_id,content,create_time)
                 VALUES ('%s','%s','%s','%s','%s','%s')
                 """%(uid,cost,type,cateid,content,time.time())
        try:
           # 执行sql语句
           self.cursor.execute(sql)
           # 提交到数据库执行
           self.db.commit()
        except Exception, e:
           print 'MYSQL ERROR:', str(e)
           print sql
           # Rollback in case there is any error
           self.db.rollback() 
    
    def insertBuildRecord(self,content):
        
        sql = """INSERT INTO item_build_record (item_type,build_item_id,name_en,name_zh,url,build_des,pop,formas,build_time)
                 VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')
                 """%(content['item_type'],content['build_item_id'],content['name_en'],content['name_zh'],content['url'],content['build_des'],content['pop'],content['formas'],content['build_time'])
        try:
           # 执行sql语句
           self.cursor.execute(sql)
           # 提交到数据库执行
           self.db.commit()
        except Exception, e:
           print 'MYSQL ERROR:', str(e)
           print sql
           # Rollback in case there is any error
           self.db.rollback() 
#wd = WarframeDB()
#print wd.getPriceByNameEnAndType('Trinity Prime Neuroptics','Blueprint')
