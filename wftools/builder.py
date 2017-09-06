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
 
    def getBuildList(self,itemName,limit =5):
        #print time.time()
        db = WarframeDB()
        itemInfo = db.getBuildItemlikeName(itemName)
        if len(itemInfo)==0:
            return '','',None
        itemType= itemInfo[0]['item_type']
        itemBuildId = itemInfo[0]['build_id']
        nameEn = itemInfo[0]['name_en']
        nameZh = itemInfo[0]['name_zh']
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
            rec['name']= self.xpathExtractFirst(tr,"td[1]/a/text()")
            rec['formas'] = self.xpathExtractFirst(tr,"td[5]/text()")
            rec['pop'] = self.xpathExtractFirst(tr,"td[7]/text()")
            rec['data'] = self.xpathExtractFirst(tr,"td[8]/text()")
            build =  self.getBuildFromUrl(rec['url'])
            rec['build'] = self.buildDictToStr(build)
            resDict.append(rec)
            #print rec['build']
        return nameEn,nameZh,resDict


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
#print wm.getBuildList('恐惧')

