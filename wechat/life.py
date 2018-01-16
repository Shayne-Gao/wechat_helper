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



print life().setKV('t1','hei')
print life().getKV('红包')


