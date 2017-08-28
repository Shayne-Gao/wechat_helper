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
class WmPricer:   

    TOP_SELLER_NUM = 3
    def getPrice(self,nameEn,itemType):
        return self.getPriceFromWm(nameEn,itemType)

    def sellerRecFormat(self,l):
        resStr = "%s : %s x %s个\n"%(l['ingame_name'],l['price'],l['count'])
        resStr = resStr.encode("utf-8")
        resStr = urllib.unquote(resStr)
        return resStr

    def getPriceFromWm(self,nameEn,itemType):
        url = 'http://warframe.market/api/get_orders/'+itemType+'/'+nameEn
        try:
            req=urllib2.Request(url)
            resp =urllib2.urlopen(req)
            html = resp.read()
            data = json.loads(html)
        except :
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
        return res
