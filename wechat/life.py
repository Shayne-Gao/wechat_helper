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

