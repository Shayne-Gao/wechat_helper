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
 
class AccountBook(object):
    def insertAccountRequest(self,request):
        #分析用户输入
        costNum,content = AccountBook().anayRequest(request)
        retStr = "已记账！\n 花费【%s】用于【%s】"%(costNum,content)
        #获取用户id等信息
        uid=1
        #推测记账内容属于什么分类
        cateid=1
        
        dbres = AccountBookDB().insertAccountRecord(uid,costNum,AccountBookDB().REC_TYPE_COST,cateid,content)      
        return retStr
    
    def anayRequest(self,request):
        request = request.decode('utf-8') # to unicode
        print type(request)
        for k,c in enumerate(request):
            if c >= '\u4e00': #and c<= '\u9fa5':
                cost=request[0:k]
                content=request[k:]
                return cost,content.encode('utf-8')
        return None
     
 
#------------------------------------------
#test()
#wf = warframe()
#print WmAlarm().getAlarmList()    
#print AccountBook().anayRequest("12.3哈哈哈123")


