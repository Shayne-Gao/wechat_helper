import json
import urlparse
import HTMLParser
import ConfigParser
import os
import urllib
import time
import MySQLdb
import sys
sys.path.append('/root/python_util')
import MyUtil
reload(sys)
sys.setdefaultencoding('utf-8')

class WsmudDB:
    db = None
    cursor = None
    dictCursor = None
    REC_TYPE_COST = 0
    REC_TYPE_INCOME = 1
    REC_VALID_TRUE = 1
    REC_VALID_FALSE = 0
    
    def __init__(self):
        (dbUser, dbPw) = MyUtil.get_db_conf()
        self.db = MySQLdb.connect('localhost', dbUser, dbPw, 'life', charset = 'utf8')
        self.cursor = self.db.cursor()
        self.dictCursor = self.db.cursor(MySQLdb.cursors.DictCursor)

    
    def queryBySql(self, sql, cursorType = 'default'):
        
        try:
            if cursorType == 'dict':
                thisCursor = self.dictCursor
            else:
                thisCursor = self.cursor
            thisCursor.execute(sql)
            self.db.commit()
            result = thisCursor.fetchall()
            return result
        except Exception:
            None
            e = None
            None
            print 'MYSQL ERROR:', str(e)
            print sql
            self.db.rollback()
            return False


    
    def getRecentRecord(self,role_id):
        sql = 'SELECT  * FROM wsmud_record where role_id = "%s" ORDER BY id DESC limit 1 '%(role_id)
       # sql = 'SELECT * FROM (SELECT * FROM `wsmud_record` ORDER BY `create_time` DESC ) `temp`  GROUP BY role_id ORDER BY `create_time`DESC '
        return self.queryBySql(sql, 'dict')

    def getAllRoldId(self):
        sql = 'SELECT DISTINCT role_id,role_menpai FROM wsmud_record GROUP BY role_id'
        return self.queryBySql(sql, 'dict')

WsmudDB().getAllRoldId()
