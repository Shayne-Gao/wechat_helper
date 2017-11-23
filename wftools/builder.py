#!/usr/bin/python
# -*- coding:utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from lxml import etree
import requests
import json
import urllib
import MySQLdb
import types
import urllib2
import time
import httplib
from db import WarframeDB
from translator import WmTranslator
from BuildStatic import BuildStatic
class WmBuilder:
    BUILD_DB_RECORD_EXPIRE_TIME = 7 * 24 * 3600 #数据库缓存的过期日期
    BUILD_RECORD_NUM = 7 #默认取多少个build记录，从这些中再经过推荐算法返回limit个
    #从url中解析build
    def getBuildFromUrl(self,url):
        urlParts = url.split('/')
        if len(urlParts) <6:
            return {}
        itemName = urlParts[5]
        buildInfos = urlParts[6].split('_')
        buildPosInfo = buildInfos[3].split('-')
        buildEnergyInfo = buildInfos[4].split('-')
        buildDict = {}
        i=0
        while i<len(buildPosInfo):
            tempDict = {}
            tempDict['pos'] =buildPosInfo[i+1]
            tempDict['lvl'] = buildPosInfo[i+2]
            buildDict[self.getModZhbyId(buildPosInfo[i])] = tempDict
            i=i+3
        i=0
        while i<len(buildEnergyInfo):
            if buildEnergyInfo[i] == 'f':
                break
            buildDict[self.getModZhbyId(buildEnergyInfo[i])]['consume'] = buildEnergyInfo[i+1]
            i = i+2
        return buildDict
    def buildDictToStr(self,buildDict):
        str = ""
        for k,v in buildDict.items():
            str += """<a href='http://warframe.huijiwiki.com/wiki/%s'>%s</a>[%s]"""%(k.decode('utf-8'),k.decode('utf-8'),v['lvl'])
            if v['pos'] == '8':
                str += '[光环]'
            str += '\n'
        return str

    def getModZhbyId(self,id):
        #print '01.'+str(time.time())
        bs = BuildStatic()
        if not id in bs.modId:
            return id;
        tsl = WmTranslator()
        res =  tsl.en2zh(bs.modId[id])
        #print '02.'+str(time.time())
        return res;
 
    #获取build的主入口
    def getBuildList(self,itemName,limit =5,source = ''):
        #获取build基本信息
        db = WarframeDB()
        itemInfo = db.getBuildItemlikeName(itemName)
        if len(itemInfo)==0:
            return '','',None
        itemType= itemInfo[0]['item_type']
        itemBuildId = itemInfo[0]['build_id']
        nameEn = itemInfo[0]['name_en']
        nameZh = itemInfo[0]['name_zh']
        #解析url中的mod装配并格式化
        #先尝试取DB的记录，如果DB没有或者太老，则取网站上的
        
        #多抓取2个，存到数据库里。但是最终只返回limit个
        
        records = self.getBuildListFromDb(itemBuildId,itemType,self.BUILD_RECORD_NUM,itemName)
        if records == [] :   
            records = self.getBuildListFromUrl(itemBuildId,itemType,nameEn,nameZh,self.BUILD_RECORD_NUM)
        #这里需要经过推荐算法，从N个中，选取M个，格式化，然后返回
        finalRecords = records[0:limit]
        for rec in finalRecords:
            build =  self.getBuildFromUrl(rec['url'])
            rec['build'] = self.buildDictToStr(build)
            rec['build_dict'] = build
        return nameEn,nameZh,finalRecords

    #从数据库缓存获取build信息 BUILD_DB_RECORD_EXPIRE_TIME
    def getBuildListFromDb(self,itemBuildId,itemType,limit,nameEn):
        startTime = time.time()
        after = time.time() - self.BUILD_DB_RECORD_EXPIRE_TIME
        res = WarframeDB().getBuildByTime(itemBuildId,itemType,after,limit)
        pTime = str(time.time() - startTime)
        logTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print "[ProcessLog][%s][Build][Item:%s][ItemType:%s][Source:DB][Ptime:%s]"%(logTime,nameEn,itemType,pTime)
        return res

    #从warframe-builder.com获取build信息
    def getBuildListFromUrl(self,itemBuildId,itemType,nameEn,nameZh,limit):
        startTime = time.time()
        #print time.time()
        bs = BuildStatic()
        typeTxt = bs.typeTxtMap[itemType]
        dataInfoPrefix = 't_30_3400020000'
        dataInfoStr = '%s/en/%s-0-%s/'%(dataInfoPrefix,itemType,itemBuildId)
        data = {"infos":dataInfoStr}
        headerStr = "http://warframe-builder.com/%s/Builder/"%(typeTxt)
        requrl = "http://warframe-builder.com/List_builds"
        headers = {
        "Referer":headerStr,
        'content-type': 'application/json;charset=UTF-8', 
        'Accept':'text/html, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'en-GB,en;q=0.8,en-US;q=0.6,zh-CN;q=0.4,zh;q=0.2',
        'Connection':'keep-alive',
        'Content-Length':'78',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Host':'warframe-builder.com',
        'Origin':'http://warframe-builder.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
        }
        dataStr = 'infos='+dataInfoStr
        dataJson = urllib.urlencode(data)
        r = requests.post(requrl, data=dataJson, headers=headers)
        #print r.text
        #print time.time()
        tree = etree.HTML(r.text)
        resTable = tree.xpath("//tr")
        resDict = []
        resCount = 0;
        for tr in resTable:
            if resCount > limit:
                break;
            
            resCount +=1
            rec= {}
            rec['url'] = self.xpathExtractFirst(tr,"td[1]/a/@href") 
            if rec['url'] == '':
                continue
            rec['build_des']= self.xpathExtractFirst(tr,"td[1]/a/text()")
            rec['formas'] = self.xpathExtractFirst(tr,"td[5]/text()")
            rec['pop'] = self.xpathExtractFirst(tr,"td[7]/text()")
            rec['build_time'] = self.xpathExtractFirst(tr,"td[8]/text()")
            #build =  self.getBuildFromUrl(rec['url'])
            #rec['build'] = self.buildDictToStr(build)
            resDict.append(rec)
            #print rec['build']
            #将url获得的结果保存到db做缓存
            rec['item_type']=itemType
            rec['build_item_id']=itemBuildId
            rec['name_en']=nameEn
            rec['name_zh']=nameZh
            rec['build_des'] = rec['build_des'].replace('\'','\\\'')
            WarframeDB().insertBuildRecord(rec)        
        pTime = str(time.time() - startTime)
        logTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print "[ProcessLog][%s][Build][Item:%s][ItemType:%s][Source:DB][Ptime:%s]"%(logTime,nameEn,itemType,pTime)

        return resDict

        
    def xpathExtractFirst(self,html,xpathStr,default=''):
        res = html.xpath(xpathStr)
        if len(res)==0:
            return default
        else:
            return res[0]
 
wm = WmBuilder()
url = 'http://warframe-builder.com/Warframes/Builder/Nekros_Prime/t_30_3400020000_2-1-10-4-7-5-7-4-5-12-5-8-37-8-5-46-6-5-54-0-10-458-2-3-527-3-3_54-7-2-6-458-9-527-9-7-9-12-7-46-11-4-9-37-7-f-f_0/en/1-0-49/130962/0'

#res = wm.getBuildFromUrl(url)
#jres = json.dumps(res, indent=1);
#print jres
# 
#print wm.getBuildList('水男')

