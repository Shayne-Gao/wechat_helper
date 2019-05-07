#!/usr/bin/python
# -*- coding:utf-8 -*- 
# 用途，按照关键字，在SMZDM的国内/海淘/发现频道中，查询最低价、最值价格和出现的日期
# 
import sys
sys.path.append("/root/python_util")
import MyUtil as Util

reload(sys)
sys.setdefaultencoding('utf-8')
import datetime
import requests
from lxml import etree
import time
from db import  LifeDB
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def getCategory():
    cate = [
        {'name':'things','cn_name':'乐事','id':1},
        {'name':'kind','cn_name':'助人','id':2},
        {'name':'work','cn_name':'工作和学习','id':3},

        {'name':'idea','cn_name':'心情/感悟','id':4},
        {'name':'special_day','cn_name':'特别的日子','id':5.1},
        {'name':'memo_day','cn_name':'纪念日','id':5.2},
        {'name':'birthday','cn_name':'生日','id':5.3},
        {'name':'encounter','cn_name':'相遇','id':5.4},
        {'name':'fun','cn_name':'娱乐/游戏','id':6},

        {'name':'news','cn_name':'关注/八卦/新闻','id':7},
        {'name':'health','cn_name':'健康/饮食','id':8},
        {'name':'dream','cn_name':'梦境','id':9},

        {'name':'relationships','cn_name':'人际关系','id':10},

        ]
    return cate

def writeDairy(cate,content,date='today'):
    if date == 'today':
        #实际上记录的是昨天的日期
        date,_ = getYesterday();
    if len(  LifeDB().setDairy(date,cate,content)) == 0:
        return True
    else:
        return False
def getDairy(date):
    return null
#获取某个分类之后的n个分类
def getRestCate(cate,num=4):
    catall=getCategory()
    catrest=[]
    find=False
    for c in catall:
        if c['name'] == cate:
            find=True
            continue
        if find:
            if len(catrest) < num:
                catrest.append(c)
    return catrest
        
def getYesterday():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
#获取昨天是星期几
    thistime=yesterday.isoweekday()
    return str(yesterday),str(thistime)

if __name__ == '__main__':
        startTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print startTime+"---------------------------------------------------------"
        print getRestCate('idea')
#        print getYesterday();
 #       print getCategory();
       # print writeDairy('helps','i m ok我好着哈哈:p!!');
