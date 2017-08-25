#!/usr/bin/python
# -*- coding:utf-8 -*-  
import json
import urllib
import MySQLdb
import types

class warframe(object):

 
    def getZhWikiUrl(self,nameZh,nameEn,itemType):
        baseUrl = 'http://warframe.huijiwiki.com/wiki/'
        pageName = ""
        tempList = nameEn.split('Prime')
        baseName = tempList[0]
        #if nameZh is not None:
        #    pageName = nameZh
        #elif nameEn is not None:
        #    pageName = nameEn
        pageName = baseName
        return baseUrl+pageName

            
    def getInfoByName(self,itemName):
        db = MySQLdb.connect("localhost","root","eas140900","warframe",charset='utf8' )

        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        sql = """SELECT * from item where name_zh like '%%%s%%' or name_en like '%%%s%%' """ %(itemName,itemName)
          # 执行SQL语句
        print sql	
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        resStr ="" 
        #print results
        if len(results)==0:
            return "未找到"+itemName+",您可以试试模糊搜索，减少搜索的字试试看"
        isFirst = True
        for r in results:
        	name_en=r[1]
        	name_zh=r[2]
        	itemType = r[3]
        	wikiZH = self.getZhWikiUrl(name_zh,name_en,itemType)
        	wikiZH = "【<a href='"+wikiZH+"'>Wiki</a>】"
        	resStr += "类别: %s\n名称: %s\n英文名: %s\n %s\n\n"%(itemType,name_zh,name_en,wikiZH)
        return resStr

    



import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#wf = warframe()
#print wf.getInfoByName('nek')

