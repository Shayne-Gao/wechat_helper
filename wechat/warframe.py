#!/usr/bin/python
# -*- coding:utf-8 -*-  
import json
import urllib
import MySQLdb
import types
import urllib2
import time
class warframe(object):

    def timestamp_datetime(self,value):
        value = int(value)
        format = '%Y-%m-%d %H:%M:%S'
        # value为传入的值为时间戳(整形)，如：1332888820
        value = time.localtime(value)
        ## 经过localtime转换后变成
        ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
        # 最后再经过strftime函数转换为正常日期格式。
        dt = time.strftime(format, value)
        return dt

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

    def getAlarm(self):
        
        req=urllib2.Request('http://deathsnacks.com/wf/data/alerts_raw.txt')
        resp =urllib2.urlopen(req)
        html = resp.read()
        alarms = html.split('\n')
        resStr = ""
        for ala in alarms:
            tempL = ala.split('|')
            if len(tempL)<9:
                continue
            starName = tempL[2]
            mapName = tempL[1]
            lvl = tempL[5] +' - '+tempL[6]
            taskType = tempL[3]
            monsType = tempL[4]
            reward = tempL[9]
            endTime = self.timestamp_datetime(tempL[8])
            resStr += "%s(%s) - %s(%s)\nLv:%s\n结束于:%s\n奖励:%s \n" %(starName,mapName,taskType,monsType,lvl,endTime,reward)
            resStr +="--------------------------\n"
        return resStr

   

    

def test():
    wf = warframe()
    print wf.getAlarm()

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#------------------------------------------
test()
#wf = warframe()
#print wf.getInfoByName('nek')


