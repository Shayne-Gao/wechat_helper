#!/usr/bin/python
# -*- coding:utf-8 -*- 

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


import scrapy
import json
import urlparse
import HTMLParser
import ConfigParser
import os
import urllib
import time
import MySQLdb
from db import AccountBookDB
class Category:

    #获取类型,会把不同别名当做不同的记录返回
    def getAllCategoryAndId(self):
        sqlRes =  AccountBookDB().getAllCategory()
        idList = []
        for res in sqlRes:
            if res[2] is not None:#has other name
                otherStr = str(res[2])
                otherName = otherStr.split('|')
                for on in otherName:
                    temp = {}
                    temp['id'] = res[0]
                    temp['name'] = on
                    temp['ori_name'] = res[1]
                    idList.append(temp);
            temp = {}
            temp['id'] = res[0]
            temp['name'] = res[1]
            temp['ori_name'] = res[1]
            idList.append(temp)
        return idList
    #获取类型 按照ID数目返回
    def getAllCategoryGroupById(self):
        sqlRes =  AccountBookDB().getAllCategory()
        idList = []
        for res in sqlRes:
            temp = {}
            temp['id'] = res[0]
            temp['name'] = res[1]
            idList.append(temp)
        return idList

    def getCategoryNameById(self,cateId):
        sqlName = AccountBookDB().getCategoryNameById(cateId)
        if sqlName is None:
            return cateId
        if len(sqlName)>=1 and sqlName[0] is not None:
            return sqlName[0]
        else:
            return cateId

    #根据记账文字的内容来猜测是属于哪个分类
    def guessCategory(self,txt):
        #1.先看是否属于【分类】【详情】的类型，如果txt以分类关键字作为开头，则直接返回
        categoryList = self.getAllCategoryAndId()
        ret = {}
        default = {}
        default['name'] = '其他'
        default['id'] = 17 
        for cate in categoryList:
            if txt.startswith(cate['name']):
                ret['name'] =  cate['ori_name']    
                ret['hit_name']=cate['name']
                ret['id'] = cate['id']    
                print cate['name']
                print cate['id']
                return ret
        return default;
        #2.再看txt中的词是否命中了关键词规则，并得出评分todo


#Category().getAllCategoryAndId();
#Category().guessCategory('打车');
#print Category().getCategoryNameById(10);
