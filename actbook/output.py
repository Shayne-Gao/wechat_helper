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
from db import AccountBookDB
from category import Category 
import datetime
from statistic import Statistic
from analysis import Analysis

from collections import defaultdict
class Output(object):
    MAX_RECORD_LIMIT=200;

    #获取最近几个月的分类信息的对比表格csv
    def getRecentMonthCateStatistic(self,recentNumber):
        year = datetime.date.today().year
        month = datetime.date.today().month
        sumPerc,sumCost = Statistic().getRecentMonthCateStatistic(recentNumber)
        allCate  = Analysis().getAllCategoryAndId()
        csvStr = ''
        csvStr += '分类'
        csvPerc = ''
        csvPerc += '分类'
        for i in range(0,recentNumber):
            csvPerc += ",%s-%s(%%)"%(year,month-i)
            csvStr += ",%s-%s(￥)"%(year,month-i)
        csvStr += "\n"
        csvPerc += "\n"
        for cate in allCate:            
            csvStr += "%s"%cate['name']
            csvPerc  += "%s"%cate['name']
            for i in range(0,recentNumber):
                thisMonth = month-i
                # print precent of cate
                try:
                    csvPerc += ',' + sumPerc[cate['name']][thisMonth] +'%'
                except KeyError:
                    csvPerc += ',0%'
                # print cost of cate
                try:
                    csvStr += ',' + str(sumCost[cate['name']][thisMonth])
                except KeyError:
                    csvStr +=',0'
            csvStr += '\n'
            csvPerc += "\n"
        return csvStr +'\n'+ csvPerc

    #获取最近几个月的明细
    def getRecentMonthRecordDetail(self,recentNumber):
        year = datetime.date.today().year
        month = datetime.date.today().month
        csvStr = ''
        for i in range(0,3):
            thisMonth = month-i
            csvStr += "%s-%s\n"%(year,month-i)
            csvStr += Statistic().getAnalysisByYearMonthAndRecord(year,thisMonth)

        return csvStr
#------------------------------------------
#test()
#wf = warframe()
#print WmAlarm().getAlarmList()    
#print AccountBook().anayRequest("12.3哈哈哈123")
#print AccountBook().getRecordByTime(0,1509608560,200,'cost')
print Output().getRecentMonthCateStatistic(3)
print Output().getRecentMonthRecordDetail(3)
