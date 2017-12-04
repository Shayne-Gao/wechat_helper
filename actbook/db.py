#!/usr/bin/env python
# encoding: utf-8
# 访问 http://tool.lu/pyc/ 查看更多信息
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
    REC_TYPE_INCOME = 1
    REC_VALID_TRUE = 1
    REC_VALID_FALSE = 0
    
    def __init__(self):
        self.db = MySQLdb.connect('localhost', 'root', 'IWLX8IS12Rl', 'accountbook', charset = 'utf8')
        self.cursor = self.db.cursor()

    
    def queryBySql(self, sql):
        
        try:
            self.cursor.execute(sql)
            self.db.commit()
            result = self.cursor.fetchall()
            return result
        except Exception:
            None
            e = None
            None
            print 'MYSQL ERROR:', str(e)
            print sql
            self.db.rollback()


    
    def getAllCategory(self):
        sql = 'SELECT * FROM account_category ORDER BY priority DESC '
        
        try:
            self.cursor.execute(sql)
            self.db.commit()
            result = self.cursor.fetchall()
            return result
        except Exception:
            None
            e = None
            None
            print 'MYSQL ERROR:', str(e)
            print sql
            self.db.rollback()


    
    def getCategoryNameById(self, cateId):
        sql = 'SELECT `name` FROM account_category WHERE id = %s limit 1' % cateId
        
        try:
            self.cursor.execute(sql)
            self.db.commit()
            result = self.cursor.fetchone()
            return result
        except Exception:
            None
            e = None
            None
            print 'MYSQL ERROR:', str(e)
            print sql
            self.db.rollback()


    
    def getSumGroupByCate(self, startTimeStamp, endTimeStamp):
        sql = 'SELECT category_id,SUM(cost) FROM account_record  WHERE UNIX_TIMESTAMP(create_time) > %s AND UNIX_TIMESTAMP(create_time) < %s AND is_valid = 1 GROUP BY category_id ORDER BY SUM(cost) DESC ' % (startTimeStamp, endTimeStamp)
        
        try:
            self.cursor.execute(sql)
            self.db.commit()
            result = self.cursor.fetchall()
            return result
        except Exception:
            None
            e = None
            None
            print 'MYSQL ERROR:', str(e)
            print sql
            self.db.rollback()


    
    def getAllRecordByTime(self, startTimeStamp, endTimeStamp, limit = 200, orderby = 'id'):
        sql = 'SELECT * FROM account_record WHERE UNIX_TIMESTAMP(create_time) > %s AND UNIX_TIMESTAMP(create_time) < %s AND is_valid = 1 order by %s  limit %s' % (startTimeStamp, endTimeStamp, orderby, limit)
        
        try:
            self.cursor.execute(sql)
            self.db.commit()
            result = self.cursor.fetchall()
            return result
        except Exception:
            None
            e = None
            None
            print 'MYSQL ERROR:', str(e)
            print sql
            self.db.rollback()


    
    def deleteLatestRecord(self, uid, isValid):
        sql = 'UPDATE account_record SET is_valid=%s WHERE  user_id=%s ORDER BY id DESC LIMIT 1' % (isValid, uid)
        return self.queryBySql(sql)

    
    def insertAccountRecord(self, uid, cost, type, cateid, content):
        sql = "INSERT INTO account_record (user_id,cost,type,category_id,content,update_time)\n                 VALUES ('%s','%s','%s','%s','%s','%s')\n                 " % (uid, cost, type, cateid, content, time.time())
        
        try:
            self.cursor.execute(sql)
            lastInsertId = self.db.insert_id()
            self.db.commit()
        except Exception:
            None
            e = None
            None
            print 'MYSQL ERROR:', str(e)
            print sql
            self.db.rollback()
            lastInsertid = 0

        return lastInsertId

    
    def insertBuildRecord(self, content):
        sql = "INSERT INTO item_build_record (item_type,build_item_id,name_en,name_zh,url,build_des,pop,formas,build_time)\n                 VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')\n                 " % (content['item_type'], content['build_item_id'], content['name_en'], content['name_zh'], content['url'], content['build_des'], content['pop'], content['formas'], content['build_time'])
        
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception:
            None
            e = None
            None
            print 'MYSQL ERROR:', str(e)
            print sql
            self.db.rollback()


