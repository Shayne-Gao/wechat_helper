#!/usr/bin/python
# -*- coding:utf-8 -*- 
import sys
reload(sys)
sys.path.append("..")
sys.setdefaultencoding('utf-8')

import json
import urllib
import MySQLdb
import types
import urllib2
import time
from wftools.translator import WmTranslator
from wftools.pricer import WmPricer
from wftools.builder import WmBuilder
class warframe(object):
    MAX_RECORD_NUM = 6 
    #MAX_RECORD_PRICE_NUM = 1 #最大查询价格的物品数目
    MAX_URL_PRICE_NUM = 2 #查询物品结果数目少于此值时，强制查询远端实时价格
    MAX_PROCESS_TIME = 3 #最大处理时间的秒数
    MAX_BUILD_NUM = 2 #获取最多的build数量
    MAX_RESPONSE_LEN = 1500 #微信最大的返回字节数目
    def timestamp_datetime(self,value):
        value = int(value)
        format = '%Y-%m-%d %H:%M:%S'
        #value为传入的值为时间戳(整形)，如：1332888820
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
    
    def getBuildlikeName(self,itemName):
        wmb = WmBuilder()
        nameEn,nameZh,buildDict = wmb.getBuildList(itemName,self.MAX_BUILD_NUM)
        if buildDict == None:
            return '未找到，请修改关键词'
        str = "%s(%s)\n"%(nameZh,nameEn)
        outputCount = 0
        for b in buildDict:
            if b['formas'] =='-':
                b['formas'] = 0
            if outputCount > self.MAX_BUILD_NUM:
                break;
            outputCount +=1
            str += '------------------------\n'
            str += "【方案%s】【极化:%s】\n"%(outputCount,b['formas'])
            str+=b['build']
            if len(str) < self.MAX_RESPONSE_LEN: 
                str+= "【<a href='"+b['url']+"'>详情</a>】\n"
            #outputCount+=1
        return str
            
    def getInfoByName(self,itemName):
        #记录开始时间
        startProcessTime = time.time()
        resStr = ""
        #尝试直接翻译
        trans = WmTranslator()
        directNameZh = trans.en2zh(itemName)
        if directNameZh != itemName:
            resStr += "您的输入也可以直接被翻译为:"+directNameZh+"\n"

        db = MySQLdb.connect("localhost","root","IWLX8IS12Rl","warframe",charset='utf8' )

        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        sql = """SELECT * from item where name_zh like '%%%s%%' or name_en like '%%%s%%' ORDER BY TYPE DESC  """ %(itemName,itemName)
          # 执行SQL语句
        #print sql   
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        #print results
        if len(results)==0:
            #尝试用输入找wiki
            wikiZH = self.getZhWikiUrl("",itemName,"")
            wikiZH = "【<a href='"+wikiZH+"'>Wiki</a>】"
            resStr += "未找到"+itemName+",您可以试试模糊搜索，减少搜索的字试试看\n尝试为您找到了"+wikiZH
            return resStr
        #这里限制长度，因为微信太长的记录显示会出错
        if len(results) > self.MAX_RECORD_NUM:
            resStr += "【提示】共搜索到%s条记录，因微信限制，只显示前%s条\n"%(len(results),self.MAX_RECORD_NUM)
            results = results[0:self.MAX_RECORD_NUM]
        isFirst = True
        pricer = WmPricer()
        checkPrice = True
        #这里限制询价的长度，因为太多的记录询价会很慢
        listCount = 0;
        priceCount = 0;
        priceSource = ''
        if len(results) <= self.MAX_URL_PRICE_NUM:
            priceSource = 'url'
        for r in results:
            name_en=r[1]
            name_zh=r[2]
            itemType = r[3]
            wikiZH = self.getZhWikiUrl(name_zh,name_en,itemType)
            wikiZH = "【<a href='"+wikiZH+"'>Wiki</a>】"
            resStr += "-------------------------------\n"
            resStr += "【%s】%s\n英文名: %s\n%s\n"%(itemType,name_zh,name_en,wikiZH)
            #get price
            listCount += 1
            #如果结果集过小，强制从api获取价格
            #如果访问已经超过阈值时间，则强制从本地获取（获取不到就返回空）
            #否则走默认的方式
            nowProcessTime = time.time()
            if nowProcessTime - startProcessTime > self.MAX_PROCESS_TIME:
                priceSource = 'db'
            itemPrice = pricer.getPrice(name_en,itemType,priceSource)
            if itemPrice is not None:
                resStr += "【最低售价"
                if itemPrice['source'] == 'url':    
                    resStr += "(实时)"
                    priceCount += 1  
                resStr +="】"
                resStr += "%s 白金\n前20平均售价：%s x %s个\n最便宜卖家：\n%s"%(itemPrice['cheapest_price'],itemPrice['top_avg'],itemPrice['top_count'],itemPrice['top_rec'])
            else:
                resStr += "未查询到售价\n"
        #是否因为时间原因未查询的物品价格？
        if priceCount < len(results): 
            resStr += "-------------------------------\n"
            resStr += "【提示】记录太多，只显示了%s个物品的实时价格，请缩小搜索范围，如wf Ash Prime Set\n"%(priceCount)
        return resStr

    def getAlarm(self):
        
        req=urllib2.Request('http://deathsnacks.com/wf/data/alerts_raw.txt')
        resp =urllib2.urlopen(req)
        html = resp.read()
        alarms = html.split('\n')
        resStr = ""
        trans = WmTranslator()
        for ala in alarms:
            tempL = ala.split('|')
            if len(tempL)<9:
                continue
            starName = trans.en2zh(tempL[2])
            mapName = tempL[1]
            lvl = tempL[5] +' - '+tempL[6]
            taskType = trans.en2zh(tempL[3])
            monsType = tempL[4]
            reward = trans.en2zh(tempL[9])
            endTime = self.timestamp_datetime(tempL[8])
            resStr += "%s(%s) - %s(%s)\nLv:%s\n结束于:%s\n奖励:%s \n" %(starName,mapName,taskType,monsType,lvl,endTime,reward)
            resStr +="--------------------------\n"
        return resStr

      
   

    

def test():
    wf = warframe()
    print wf.getBuildlikeName('lenz')
#------------------------------------------
#test()
#wf = warframe()




