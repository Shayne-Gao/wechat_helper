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
from category import Category
class Analysis:

    def getPercent(self,startStamp,endStamp,limit,costType=0):
        #res = AccountBookDB().getAllRecordByTime(startStamp,endStamp,limit);
        res = AccountBookDB().getSumGroupByCate(startStamp,endStamp,costType);
        typeMap = {}
        costSum = 0;
        if res is None:
            return "Not found record!"
        else:
            for record in res:
                costSum += record[1]
        resList = []
        for k in res:
            temp = {}
            temp['cateId'] = k[0]
            temp['name'] = Category().getCategoryNameById(k[0])
            temp['cost'] = k[1]
            temp['percent'] = "%.2f"%(k[1]/costSum * 100)
            resList.append(temp)    

        return resList

    def getNoRecordCate(self,recordList):
          #获取其他么有记录的分类
        otherCat = Analysis().getAllCategoryAndId()
        for k in recordList:
             #获取其他么有记录的分类,如果有记录，就从other里删除
            for cat in otherCat:
                if cat['id'] == k['cateId']:
                    cat['id'] = -1 #mark to id=-1
        resList = []
        for cat in otherCat:
            if cat['id'] != -1:
                resList.append(cat)
        print resList
        return resList    

    #获取所有的分类，注意，这里会将分类的别名当做一个单独的分类返回,所以ID不唯一
    def getAllCategoryAndId(self):
        sqlRes =  AccountBookDB().getAllCategory()
        idList = []
        for res in sqlRes:
           # if res[2] is not None:#has other name
            #    otherStr = str(res[2])
             #   otherName = otherStr.split('|')
              #  for on in otherName:
               #     temp = {}
                #    temp['id'] = res[0]
                 #   temp['name'] = on
                  #  temp['ori_name'] = res[1]
                   # idList.append(temp);
            temp = {}
            temp['id'] = res[0]
            temp['name'] = res[1]
            temp['other_name'] = res[2]
            temp['ori_name'] = res[1]
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
            #比较分类名字
            if txt.startswith(cate['name']):
                ret['name'] =  cate['ori_name']    
                ret['hit_name']=cate['name']
                ret['id'] = cate['id']    
                print cate['name']
                print cate['id']
                return ret
            #比较other name
            otherNameList = otherStr.split('|')
            for on in otherNameList:
                if txt.startswith(on):
                    ret['name'] =  cate['ori_name']
                    ret['hit_name']=cate['name']
                    ret['id'] = cate['id']
                    return ret
        return default;
        #2.再看txt中的词是否命中了关键词规则，并得出评分todo


#Category().getAllCategoryAndId();
#Category().guessCategory('打车');
#print Category().getCategoryNameById(10);
#print Analysis().getPercent(0,1509693496,1)
