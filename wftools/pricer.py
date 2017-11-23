#!/usr/bin/python
# -*- coding:utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import urllib
import MySQLdb
import types
import urllib2
import time
import datetime
import httplib 
from db import WarframeDB
class WmPricer:   
    DB_PRICE_EXPIRE_TIME = 3 * 60 #100秒之前的DB数据不再生效
    PIRCE_STATISTIC_COUNT_MIN = 20 #只有当价格记录大于这个值，才会计算最高最低价格
    TOP_SELLER_NUM = 3
    def getPrice(self,nameEn,itemType,source=''):
        #logTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        #print "[ProcessLog][%s][Price][Req:%s][Source:DB]"
        if source =='url':
            return self.getPriceFromWm(nameEn,itemType)
        elif source =='db':
            return self.getPriceFromDb(nameEn,itemType)
        else:#默认获取方式
            dbprice = self.getPriceFromDb(nameEn,itemType)
            if dbprice is None:
                return self.getPriceFromWm(nameEn,itemType)
            else:
                #str to datetime, then datetime to timestamp and compare 
                dataRecordTime = datetime.datetime.strptime(dbprice['record_time'], "%Y-%m-%d %H:%M:%S")
                timeArray = dataRecordTime.timetuple()
                #timeArray = time.strptime(rtime, "%Y-%m-%d %H:%M:%S")
                timeStamp = int(time.mktime(timeArray))
                nowTimeStamp = int(time.time())
                if nowTimeStamp - timeStamp > self.DB_PRICE_EXPIRE_TIME:
                    #说明db的记录太老，强制从url获取
                    return self.getPriceFromWm(nameEn,itemType)
                else:
                    return dbprice


    def sellerRecFormat(self,l):
        resStr = "%s : %s x %s个\n"%(l['ingame_name'],l['price'],l['count'])
        resStr = resStr.encode("utf-8")
        resStr = urllib.unquote(resStr)
        return resStr
    
    def getPriceFromDb(self,nameEn,itemType):
        wfdb = WarframeDB()
        startTime = time.time()
        dbprice = wfdb.getPriceByNameEnAndType(nameEn,itemType)
        if dbprice is not None:
            dbprice['top_rec'] = dbprice['top_rec'].replace('|','个\n')
            dbprice['top_rec'] = dbprice['top_rec'].replace(':',' : ')
        pTime = str(time.time() - startTime)
        logTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print "[ProcessLog][%s][Price][Item:%s][ItemType:%s][Source:DB][Ptime:%s]"%(logTime,nameEn,itemType,pTime)
        return dbprice

    def getPriceFromWm(self,nameEn,itemType):   
        startTime = time.time()
        nameEnQuote = urllib.quote(nameEn)
        url = 'http://warframe.market/api/get_orders/'+itemType+'/'+nameEnQuote
        try:
            req=urllib2.Request(url)
            resp =urllib2.urlopen(req)
            html = resp.read()
            
            #conn = httplib.HTTPConnection('warframe.market')
            #conn.request('GET','/api/get_orders/'+itemType+'/'+nameEn)
            #html = conn.getresponse()

            data = json.loads(html)
        except :
            print url
            return None
        if data['code'] != 200:
            return None
        sellInfo = data['response']['sell'];
        if len(sellInfo) ==0:
            return None
        #get online player records
        onlineSellRec = []
        onlineSellRecSum = 0
        onlineSellRecCount = 0
        for info in sellInfo:
            if info['online_ingame'] == False:
                continue
            #ignore xbox and ps4 record
            nameStr = info['ingame_name'].encode("utf-8")
            nameStr = urllib.unquote(nameStr)
            if nameStr.startswith('(PS4)') or nameStr.startswith('(XB1)'):
                continue
            #else
            onlineSellRec.append(info)
            onlineSellRecSum += info['price'] * info['count']
            onlineSellRecCount += info['count']
        #sort and analysis
        if len(onlineSellRec) ==0:
            return None
        onlineSellRec.sort(key=lambda obj:obj.get('price'), reverse=False)
        res = {}
        res['top_rec'] ="" 
        topSellerSum = min(self.TOP_SELLER_NUM,len(onlineSellRec))
        for i in range(0,topSellerSum):
            strT = self.sellerRecFormat(onlineSellRec[i])
            res['top_rec'] += strT
        res['cheapest_price'] = onlineSellRec[0]['price']
        res['all_count'] = onlineSellRecCount
        res['all_avg'] = onlineSellRecSum / onlineSellRecCount

        topSum = 0
        topCount = 0
        for rec in onlineSellRec[0:20]:
            topSum += rec['price'] * rec['count']
            topCount += rec['count']
        res['top_count'] = topCount
        res['top_sum'] = topSum
        res['top_avg'] = topSum / topCount
        res['record_time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        res['source']='url'
        #查询结果计入数据库
        wfdb = WarframeDB()
        itemIdName = wfdb.getItemLikeName(nameEn)
        res['itemId']=itemIdName[0]['id']
        res['item'] = nameEn
        res['category'] = itemIdName[0]['type']
        wfdb.insertPrice(res)
        pTime = str(time.time() - startTime)
        logTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print "[ProcessLog][%s][Price][Item:%s][ItemType:%s][Source:WM][Ptime:%s]"%(logTime,nameEn,itemType,pTime)
        return res
    
    #获取物品前段时间的最高价和最低价，只有在价格记录数目大于阈值的时候才查询
    def getPriceSimpleStatistic(self,nameEn,gapTime):
        gapTimeStamp = int(time.time() - gapTime)
        getRecSql = "SELECT cheapest_price,record_time FROM item_price_record WHERE name_en = '%s' AND UNIX_TIMESTAMP(record_time)>'%s' order by record_time asc "%(nameEn,gapTimeStamp)
        records = WarframeDB().queryBySql(getRecSql);
       #PIRCE_STATISTIC_COUNT_MIN = 20 #只有当价格记录大于这个值，才会计算最高最低价格
        if len(records) < self.PIRCE_STATISTIC_COUNT_MIN:
            return None
        highest = 0;
        lowest = 9999;
        sumP = 0;
        for r in records:
            highest = max(r[0],highest)
            lowest = min(r[0],lowest)
            sumP += r[0]
        res = {}
        res['highest'] = highest
        res['lowest'] = lowest
        res['avg'] = sumP / len(records) 
        return res

#wm = WmPricer()
#print WmPricer().getPriceSimpleStatistic('Ash Prime Set', 3*24*3600)
