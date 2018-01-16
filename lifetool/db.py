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
import sys
sys.path.append("/root/python_util")
import MyUtil as MyUtil
reload(sys)
sys.setdefaultencoding('utf-8')
class LifeDB:
    db = None
    cursor = None
    dictCursor = None
    REC_TYPE_COST = 0
    REC_TYPE_INCOME = 1
    REC_VALID_TRUE = 1
    REC_VALID_FALSE = 0
    
    def __init__(self):
        dbUser,dbPw = MyUtil.get_db_conf()
        self.db = MySQLdb.connect('localhost', dbUser, dbPw,'life', charset = 'utf8')
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
            return False
   
    def setKV(self,key,value):
        sql = "INSERT INTO kv_store  (`key`,`value`) VALUES ('%s','%s')  ON DUPLICATE KEY UPDATE VALUE='%s'"%(key,value,value)
        return self.queryBySql(sql)

    def getKV(self,key):
        sql = "SELECT `key`,`value` from kv_store where `key` like '%%%s%%' order by ctime "%(key)
        return self.queryBySql(sql,'dict')

print LifeDB().getKV('红包')
