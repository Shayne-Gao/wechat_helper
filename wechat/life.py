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
from lifetool.db import LifeDB
import lifetool.dairy as dairy
class life():
    def scarf(self,line):
        #line =int( sys.argv[1])
        line = int(line)
        pattern = line % 12
        patternSingle = (pattern+1) / 2
        patternList = ['---+++','+---++','++---+','+++---','-+++--','--+++-']
        printLenth = 12
        currentPattern = patternList[patternSingle-1]
        if line % 2 ==1:
            currentPattern = 'v'+currentPattern[1:]
        print currentPattern
        return currentPattern
    #1 ---+++
    #2 --+++
    #3 -+++
    #4 +++
    #5 ++
    def getDairyCate(self):
        cateStr = ''
        cate = dairy.getCategory()
        for c in cate:
            if c['id'] < 10:
                cateStr += "<a>" + c['name']+"</a>--->"+c['cn_name'] + "\n"
        date,week = dairy.getYesterday()
        cateStr += "将会记录【"+date+"】星期【"+week+"】的日记哦"
        return cateStr
    
    def writeDairy(self,content):
        #获取cate
        if len(content) < 5:
            return "写点什么吧" 
        cate = dairy.getCategory()
        contentCate = ''
        for c in cate:
            if c['name'].startswith(content[3]):
                contentCate = c['name']
                cateName = c['cn_name']
                break
        if contentCate == '':
            return '分类不对噢，输入英文名第一个字母'
        if dairy.writeDairy(contentCate,content[4:]):
            catRest = dairy.getRestCate(contentCate)
            retStr = '已记录【'+cateName+'】! next...\n'
            for c in catRest:
                retStr +="<a>" + c['name'] + "</a> --->" + c['cn_name'] +"\n"
            return retStr
        else:
            return '出错啦'
        
    def setKV(self,key,value):
        res = LifeDB().setKV(key,value);
        if res is not False:
            return True
        else:
            return False


    def getKV(self,key):
        res = LifeDB().getKV(key)
        if len(res)==0 or res is False or 'value' not in res[0]:
            return False
        else:
            resStr = ''
            for r in res:
                resStr += '%s : %s\r\n'%(r['key'],r['value'])
            return resStr

life().getDairyCate()

