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
from lifetool.excel import ExcelTool
from lifetool import price

class LifeTool():
    def getItemPrice(self,key):
        res =  price.getItemInfo(key,'youhui') +  price.getItemInfo(key,'faxian') +  price.getItemInfo(key,'haitao')
        for r in res:
            if r['uprate'] > 90:
                r['bgcolor'] = '#ff8080'
            elif r['uprate'] > 75:
                r['bgcolor'] = '#ffff4d'
            else:
                r['bgcolor'] = '#e5f2ff'
            #r['time'] = r['time'].split(' ')[0]
        return res

    def getSBNContent(self,eid,startDate,firstYearBonus,secondYearBonus):
        return ExcelTool().getSBNContent(eid,startDate,firstYearBonus,secondYearBonus)

    def getSBNTitle(self):
        return ExcelTool().getSBNTitle()

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
#print LifeTool().getItemPrice('移动硬盘 2t')
