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
    dictCursor = None
    REC_TYPE_COST = 0
    REC_TYPE_INCOME = 1
    REC_VALID_TRUE = 1
    REC_VALID_FALSE = 0
    
    def __init__(self):
        self.db = MySQLdb.connect('localhost', 'root', 'IWLX8IS12Rl', 'accountbook', charset = 'utf8')
        self.cursor = self.db.cursor()
        self.dictCursor = self.db.cursor(MySQLdb.cursors.DictCursor)
    
    def queryBySql(self, sql,cursorType='default'):
        try:
            if cursorType =='dict':
                thisCursor = self.dictCursor
            else:
                thisCursor = self.cursor
            thisCursor.execute(sql)
            self.db.commit()
            result = thisCursor.fetchall()
            return result
        except Exception as e:
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
            e = None
            print 'MYSQL ERROR:', str(e)
            print sql
            self.db.rollback()
    
    def updateLastRecordCate(self,uid,cateId):
        sql = 'UPDATE account_record SET category_id=%s, update_time=CURRENT_TIMESTAMP WHERE  user_id=%s and is_valid=1 ORDER BY id DESC LIMIT 1' % (cateId, uid)
        return self.queryBySql(sql)
    

    def getCategoryIdByNameAndOtherName(self,cateName):
        sql = ''' SELECT id FROM account_category WHERE NAME = '%s' OR other_name LIKE '%%%s%%' LIMIT 1 ''' % (cateName,cateName)
        result =  self.queryBySql(sql)
        if len(result) >0:
            return result[0][0]
        else:
            return None


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

    #获取最后一条有效的记账记录
    def getLastValidRecord(self,uid):
        sql = 'SELECT * from account_record where user_id =%s and is_valid = 1 ORDER BY id DESC limit 1'%(uid)
        res =  self.queryBySql(sql,'dict')
        if len(res) >0 :
            return res[0]
        else:
            return None


    def deleteLatestRecord(self, uid, isValid):
        sql = 'UPDATE account_record SET is_valid=%s, update_time=CURRENT_TIMESTAMP WHERE  user_id=%s ORDER BY id DESC LIMIT 1' % (isValid, uid)
        return self.queryBySql(sql)

    
    def insertAccountRecord(self, uid, cost, type, cateid, content):
        sql = "INSERT INTO account_record (user_id,cost,type,category_id,content,create_time)    VALUES ('%s','%s','%s','%s','%s','%s')    " % (uid, cost, type, cateid, content, time.time())
        
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


