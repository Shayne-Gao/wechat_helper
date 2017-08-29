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

class WarframeDB:
    db = None
    cursor = None

    def __init__(self):
        self.db = MySQLdb.connect("localhost","root","IWLX8IS12Rl","warframe",charset='utf8' )
        self.cursor = self.db.cursor()

    def getItemLikeName(self,itemName):
        sql = """SELECT id,name_en,type from item where name_zh like '%%%s%%' or name_en like '%%%s%%' """ %(itemName,itemName)
          # 执行SQL语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        resList = []
        #print results
        if len(results)==0:
            return resList
        for r in results:
            temp = {}
            temp['id']=r[0]
            temp['name_en']=r[1]
            temp['type']=r[2]
            resList.append(temp)
        return resList

    def getPriceByNameEnAndType(self,nameEn,Type):
        sql = """SELECT * from item_price_record where name_en = '%s' and type ='%s' limit 1 """ %(nameEn,Type)
          # 执行SQL语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        content = {}
        #print results
        if len(results)==0:
            return None
        res = results[0]
        content['itemId'] = res[1]
        content['item'] = res[2]
        content['type'] = res[3]
        content['cheapest_price'] = res[4]
        content['top_avg'] = res[5]
        content['top_count'] = res[6]
        content['all_avg'] = res[7]
        content['all_count'] = res[8]
        content['record_time'] = res[11]
        content['top_rec']  = res[9]         
        content['source'] = 'db'
        return content

    def insertPrice(self,content):
        #get item id
     
        sql = """INSERT INTO item_price_record (item_id,name_en,type, cheapest_price,top_avg,top_count,all_avg,all_count,record_time,top_rec)
                 VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
                 """%(content['itemId'],content['item'],content['category'],content['cheapest_price'],content['top_avg'],content['top_count'],content['all_avg'],content['all_count'],content['record_time'],content['top_rec'])
        try:
           # 执行sql语句
           print sql
           self.cursor.execute(sql)
           # 提交到数据库执行
           self.db.commit()
        except:
           # Rollback in case there is any error
           self.db.rollback()
  
#wd = WarframeDB()
#print wd.getPriceByNameEnAndType('Trinity Prime Neuroptics','Blueprint')
