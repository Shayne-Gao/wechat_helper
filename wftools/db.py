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

    def queryBySql(self,sql):
          # 执行SQL语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        self.db.commit()
        results = self.cursor.fetchall()
        return results
    def getBuildItemlikeName(self,itemName):
        sql = """SELECT id,name_en,name_zh,item_type,build_id from build_item where name_zh like '%%%s%%' or name_en like '%%%s%%' """ %(itemName,itemName)
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
            temp['name_zh']=r[2]
            temp['item_type']=r[3]
            temp['build_id'] = r[4]
            resList.append(temp)
        return resList

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
        #默认获取最新的一条记录
        sql = """SELECT * from item_price_record where name_en = '%s' and type ='%s' order by record_time desc limit 1 """ %(nameEn,Type)
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
        #recordTime = time.strftime('%Y-%m-%d %H:%M:%S',res[11].timetuple())
        #datetime to str, for same construct with get from wm
        recordTime = res[11].strftime('%Y-%m-%d %H:%M:%S')
        content['record_time'] = recordTime
        content['top_rec']  = res[9]         
        content['source'] = 'db'
        return content
    def getBuildByTime(self,itemBuildId,itemType,afterUnixTimestamp,limit):
        sql = """ SELECT * FROM item_build_record WHERE item_type=%s AND build_item_id=%s AND UNIX_TIMESTAMP(record_time)>'%s' GROUP BY build_des order by record_time desc LIMIT %s """%(itemType,itemBuildId,afterUnixTimestamp,limit)
        # 执行SQL语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        results = self.cursor.fetchall()
        content =[] 
        for res in  results:
            one = {}
            one['url'] = res[5]
            one['build_des'] = res[6]
            one['formas'] = res[8]
            one['pop'] = res[7]
            one['build_time']  = res[10]   
            content.append(one)
        return content
 
    def insertPrice(self,content):
        #get item id
     
        sql = """INSERT INTO item_price_record (item_id,name_en,type, cheapest_price,top_avg,top_count,all_avg,all_count,record_time,top_rec)
                 VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')
                 """%(content['itemId'],content['item'],content['category'],content['cheapest_price'],content['top_avg'],content['top_count'],content['all_avg'],content['all_count'],content['record_time'],content['top_rec'])
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
