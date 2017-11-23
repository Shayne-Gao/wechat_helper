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
from actbook.db import AccountBookDB
from wftools.db import WarframeDB
from actbook.category import Category 
import datetime
from actbook.analysis import Analysis
class AccountBook(object):
    MAX_RECORD_LIMIT=200;
    def insertAccountRequest(self,request):
        #分析用户输入
        costNum,content = AccountBook().anayRequest(request)
        #获取用户id等信息
        uid=1
        #推测记账内容属于什么分类
        cateidList=Category().guessCategory(content);
        if cateidList is not None:
            cateid = cateidList['id']
            cateTxt = cateidList['name']
        else:
            cateid = 0
            cateTxt = '未分类'
        retStr = "已记账！\n花费【%s】用于【%s】\n分类【%s】"%(costNum,content,cateTxt);
        dbres = AccountBookDB().insertAccountRecord(uid,costNum,AccountBookDB().REC_TYPE_COST,cateid,content)      
        if dbres != 0 and dbres is not None:
            retStr = "已记账！\n花费【%s】用于【%s】\n分类【%s】【%s】"%(costNum,content,cateTxt,dbres);
        else:
            retStr = "记账失败"
        return retStr
    
    def anayRequest(self,request):
        request = request.decode('utf-8') # to unicode
        for k,c in enumerate(request):
            if c >= '\u4e00': #and c<= '\u9fa5':
                cost=request[0:k]
                content=request[k:]
                return cost,content.encode('utf-8')
        return None
    def getRecordByYearMonth(self,year,month,orderby='id'):
        start = "%s-%s-01 00:00:00"%(year,month)    
        end = "%s-%s-01 00:00:00"%(year,int(month)+1)
        startStamp = time.mktime(time.strptime(start,"%Y-%m-%d %H:%M:%S")) 
        endStamp = time.mktime(time.strptime(end,"%Y-%m-%d %H:%M:%S")) 
        return self.getRecordByTime(int(startStamp),int(endStamp),self.MAX_RECORD_LIMIT,orderby)

    def deleteLatestRecord(self,uid,valid=AccountBookDB().REC_VALID_FALSE):
        return    AccountBookDB().deleteLatestRecord(1,valid)

    #获得带样式的分类统计信息
    def getAnalysisByYearMonth(self,year,month):
        responseStr = ""
        start = "%s-%s-01 00:00:00"%(year,month)
        end = "%s-%s-01 00:00:00"%(year,int(month)+1)
        startStamp = time.mktime(time.strptime(start,"%Y-%m-%d %H:%M:%S"))
        endStamp = time.mktime(time.strptime(end,"%Y-%m-%d %H:%M:%S"))
        res =  Analysis().getPercent(int(startStamp),int(endStamp),self.MAX_RECORD_LIMIT)
        totalCost = 0
        for r in res:
            markNum = int(float( r['percent'])) / 1+1
            mark = '';
            for i in range(0,markNum):
                mark += "|"
            totalCost+=r['cost']
            responseStr += "【%s】%8s%%   ￥%s\n%s\n"%(r['name'],r['percent'],r['cost'],mark)
        responseStr +="【总花费】￥%s\n\n"%(totalCost)
        #获取其他没记录的分类列表
        otherList =  Analysis().getNoRecordCate(res)
        responseStr += "---------------\n以下分类无记录\n"
        for r in otherList:
            responseStr += "【%s】\n"%r['name']
        return responseStr

    #获得带样式的分类统计信息+各类别的明细
    def getAnalysisByYearMonthAndRecord(self,year,month):
        responseStr = ""
        start = "%s-%s-01 00:00:00"%(year,month)
        end = "%s-%s-01 00:00:00"%(year,int(month)+1)
        startStamp = time.mktime(time.strptime(start,"%Y-%m-%d %H:%M:%S"))
        endStamp = time.mktime(time.strptime(end,"%Y-%m-%d %H:%M:%S"))
        res =  Analysis().getPercent(int(startStamp),int(endStamp),self.MAX_RECORD_LIMIT)
        resRecord = AccountBookDB().getAllRecordByTime(startStamp,endStamp,self.MAX_RECORD_LIMIT,'category_id,cost desc');
        for r in res:
            markNum = int(float( r['percent'])) / 1+1
            mark = '';
            for i in range(0,markNum):
                mark += "|"
            responseStr += '----------------------------\n'
            responseStr += "【%s】%10s%%   ￥%s\n"%(r['name'],r['percent'],r['cost'])
            #显示这个分类下的明细
            for record in resRecord:
                if len(record)<6:
                    continue
                if Category().getCategoryNameById(record[4]) != r['name']:
                    continue
                if record[2] < 1:  #因为微信有最大返回行数，所以小于阈值的详情不在统计内显示
                    continue
                responseStr += "%s | ￥% 7.2f | %s\n"%(record[6].strftime('%d日'),record[2],record[5])    
        return responseStr



    def getRecordByTime(self,startTime,endTime,limit,orderby):
        responseStr = "";
        res = AccountBookDB().getAllRecordByTime(startTime,endTime,limit,orderby);
        if res is None:
            return "Not found record!"
        else:
            for record in res:
                if len(record)<6:
                    continue
                recordId = record[0]
                userId = record[1]
                cost = record[2]
                type = record[3]
                cateId = record[4]
                content = record[5]
                createTime = record[6]
                outputStr = "%s | ￥% 7.2f | %s(%s)\n"%(createTime.strftime('%d日'),cost, Category().getCategoryNameById(cateId),content)
                responseStr += outputStr
            return responseStr
 
#------------------------------------------
#test()
#wf = warframe()
#print WmAlarm().getAlarmList()    
#print AccountBook().anayRequest("12.3哈哈哈123")
#print AccountBook().getRecordByTime(0,1509608560,200,'cost')
#print AccountBook().getAnalysisByYearMonth(datetime.date.today().year,10)
#print AccountBook().getAnalysisByYearMonthAndRecord(datetime.date.today().year,11)
#print AccountBook().deleteLatestRecord(1)
