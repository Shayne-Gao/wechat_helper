# -*- coding:utf-8 -*- 
# uncompyle6 version 2.14.0

# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.5 (default, Nov  6 2016, 00:28:07) 
# [GCC 4.8.5 20150623 (Red Hat 4.8.5-11)]
# Embedded file name: ../actbook/statistic.py
# Compiled at: 2017-12-04 17:22:24
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json, urllib, MySQLdb, types, urllib2, time
from db import AccountBookDB
import datetime
from category import Category
from analysis import Analysis
from collections import defaultdict

class Statistic(object):
    MAX_RECORD_LIMIT = 200

    def getRecordByYearMonth(self, year, month, orderby='id'):
        start = '%s-%s-01 00:00:00' % (year, month)
        end = '%s-%s-01 00:00:00' % (year, int(month) + 1)
        startStamp = time.mktime(time.strptime(start, '%Y-%m-%d %H:%M:%S'))
        endStamp = time.mktime(time.strptime(end, '%Y-%m-%d %H:%M:%S'))
        return self.getRecordByTime(int(startStamp), int(endStamp), self.MAX_RECORD_LIMIT, orderby)

    #获取某一个月按照分类的统计信息（金额，百分比，总量)
    def getAnalysisByYearMonth(self, year, month,costType=0):
        responseStr = ''
        start = '%s-%s-01 00:00:00' % (year, month)
        if int(month) + 1 > 12:
            endYear = int(year) + 1
            endMonth = 1
        else:
            endYear = year
            endMonth = int(month) + 1
        end = '%s-%s-01 00:00:00' % (endYear, endMonth)
        startStamp = time.mktime(time.strptime(start, '%Y-%m-%d %H:%M:%S'))
        endStamp = time.mktime(time.strptime(end, '%Y-%m-%d %H:%M:%S'))
        res = Analysis().getPercent(int(startStamp), int(endStamp), self.MAX_RECORD_LIMIT,costType)
        totalCost = 0
        perc = {}
        cost = {}
        for r in res:
            totalCost += r['cost']
            perc[r['name']] = r['percent']
            cost[r['name']] = r['cost']

        return (perc, cost, totalCost)

    #获取每月的详情记录(按照分类排序)
    def getAnalysisByYearMonthAndRecord(self, year, month,costType=0):
        responseStr = ''
        start = '%s-%s-01 00:00:00' % (year, month)
        if int(month) + 1 > 12:
            endYear = int(year) + 1
            endMonth = 1
        else:
            endYear = year
            endMonth = int(month) + 1
        end = '%s-%s-01 00:00:00' % (endYear, endMonth)
        startStamp = time.mktime(time.strptime(start, '%Y-%m-%d %H:%M:%S'))
        endStamp = time.mktime(time.strptime(end, '%Y-%m-%d %H:%M:%S'))
        res = Analysis().getPercent(int(startStamp), int(endStamp), self.MAX_RECORD_LIMIT,costType)
        resRecord = AccountBookDB().getAllRecordByTime(startStamp, endStamp, self.MAX_RECORD_LIMIT, 'category_id,cost desc')
        
        for r in res:
            for record in resRecord:
                if len(record) < 6:
                    continue
                if Category().getCategoryNameById(record[4]) != r['name']:
                    continue
                responseStr += '%s,%.2f,%s,%s\n' % (record[6], record[2], record[5],r['name'])

        return responseStr

    def getRecordByTime(self, startTime, endTime, limit, orderby):
        responseStr = ''
        res = AccountBookDB().getAllRecordByTime(startTime, endTime, limit, orderby)
        if res is None:
            return 'Not found record!'
        else:
            for record in res:
                if len(record) < 6:
                    continue
                recordId = record[0]
                userId = record[1]
                cost = record[2]
                type = record[3]
                cateId = record[4]
                content = record[5]
                createTime = record[6]
                outputStr = '%s | \xef\xbf\xa5% 7.2f | %s(%s)\n' % (createTime.strftime('%d\xe6\x97\xa5'), cost, Category().getCategoryNameById(cateId), content)
                responseStr += outputStr

            return responseStr
            return

    def getRecentDate(nowYear,nowMonth,recentNumber):
        
        for i in range(0,recentNumber):
            thisMonth = nowMonth - i
            if thisMonth <1:
                thisMonth = 12 + thisMonth
                thisYear = nowYear - 1
            else:
                thisYear = nowYear
    def getRecentMonthCateStatistic(self, recentNumber):
        year = datetime.date.today().year
        month = datetime.date.today().month
        sumPerc = defaultdict(dict)
        sumCost = defaultdict(dict)
        for i in range(0, recentNumber):
            thisMonth = month - i
            if thisMonth < 1:
                thisMonth = 12 +  thisMonth
                thisYear = year -1
            else:
                thisYear = year
            perc, cost, totalCost = Statistic().getAnalysisByYearMonth(thisYear, thisMonth)
            for name, v in perc.items():
                sumPerc[name][thisMonth] = v

            for name, v in cost.items():
                sumCost[name][thisMonth] = v
            sumCost['总计'][thisMonth] = totalCost
        return (sumPerc, sumCost)
# okay decompiling statistic.pyc
