#!/usr/bin/python
## -*- coding:utf8 -*-
import sys     
reload(sys)    
sys.setdefaultencoding('utf8')    

import json
import urllib
import MySQLdb
import types
import os
class WmTranslator:
    transDict = {}
    def __init__(self):
        BASE_DIR = os.path.dirname(__file__) #获取当前文件夹的绝对路径
        file_path = os.path.join(BASE_DIR, 'en2zh.dict') #获取当前文件夹内的Test_Data文件
        file = open(file_path,'r')
        line = file.readline()
        while line:
            line = file.readline()
            l = line.split('=')
            if(len(l)<2):
                    continue
            lt = l[1].split('\n')
            l[1] = lt[0]
            self.transDict[l[0].lower()] = l[1]
            if not line:
                    break
            pass # do something
    def en2zh(self,nameEn):
        words = nameEn.split(' ')
        lens = len(words)
        resZh = ""
        startIndex = 0
        #单词是否可以直接翻译，如果可以就返回
        zhWordDir = self.transDict.get(nameEn.lower())
        if zhWordDir is not None:            
            #取出回车
            return zhWordDir.replace('\r','') 
        while(startIndex < lens):
            #单词有直接翻译，就翻译
            nowWord = ""
            for endIndex in range(startIndex,lens):
                #组合成新的分词
                nowWord += words[endIndex].lower()
                #print nowWord
                #check
                zhWord = self.transDict.get(nowWord)
                if zhWord is not None:
                    tempL = zhWord.split('\r')
                    zhWord = tempL[0]
                    if resZh == "":
                        resZh += zhWord
                    else:
                        resZh += " "+zhWord
                    #print zhWord
                    startIndex += endIndex - startIndex
                    #print 'found:'+resZh
                    break
                #what if cannot found at last
                if endIndex == lens-1:
                    if resZh == "":
                        resZh += words[startIndex]
                    else:
                        resZh += " "+words[startIndex]
                nowWord += " "
            startIndex += 1
        return resZh

#tsl = WmTranslator()
#print tsl.en2zh(sys.argv[1])
#print trans(sys.argv[1])






