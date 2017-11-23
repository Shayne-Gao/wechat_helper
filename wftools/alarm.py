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
 

class WmAlarm:
    def getAlarmList(self):
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


    def getSorties(self):
        modifier = {
        'SORTIE_MODIFIER_PUNCTURE':'穿刺伤害强化',
        'SORTIE_MODIFIER_EXIMUS':'卓越者据点',
        'SORTIE_MODIFIER_HAZARD_RADIATION':'辐射灾害',
        'SORTIE_MODIFIER_LOW_ENERGY':'能量衰减',
        'SORTIE_MODIFIER_FREEZE':'寒冰',
        }
        req=urllib2.Request('http://deathsnacks.com/wf/data/sorties.json')
        resp =urllib2.urlopen(req)
        html = resp.read()
        data = json.loads(html)
        infos = data['Variants']
        resStr = ""
        for s in  infos:
            tempS = s['node'].split(' (')
            mapName = tempS[0]
            starName = WmTranslator().en2zh(tempS[1].replace(')',''))
            resStr+="%s(%s) - %s [%s]\n"%(starName,mapName,WmTranslator().en2zh(s['missionType']),modifier.get(s['modifierType'],s['modifierType']))
        return resStr

    def getInvasionList(self):
        #http://deathsnacks.com/wf/data/invasion_raw.txt
        req=urllib2.Request('http://deathsnacks.com/wf/data/invasion_raw.txt')
        resp =urllib2.urlopen(req)
        html = resp.read()
        alarms = html.split('\n')
        resStr = ""
        trans = WmTranslator()
        for ala in alarms:
            tempL = ala.split('|')
            if len(tempL)<17:
                continue
            starName = trans.en2zh(tempL[2])
            mapName = tempL[1]
            if tempL[5] =='0cr':
                left = tempL[3]
            else:
                left = tempL[3] +'('+trans.en2zh(tempL[5])+')'
            right = tempL[8] +'('+trans.en2zh(tempL[10])+')'

       
            endTime = self.timestamp_datetime(tempL[13])
            process = tempL[14]+'vs'+tempL[15]
            if float(tempL[16]) <= 0:
                process = "已完成"
            else:
                leftPrecent = tempL[16] +'%'
                rightPercent = str(100.00 -float( tempL[16])) +'%'
                process = "%s    vs     %s"%(leftPrecent,rightPercent)
            estTime = tempL[17].replace('ETA: ','')
            invName = trans.en2zh(tempL[18])

            resStr += "%s(%s) - %s \n %s vs %s\n %s \n 预计持续:%s\n"%(starName,mapName,invName,left,right,process,estTime)
            resStr +="--------------------------\n"
        return resStr

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

#print WmAlarm().getInvasionList()
#print WmAlarm().getSorties()
