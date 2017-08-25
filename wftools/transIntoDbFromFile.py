#!/usr/bin/python
## -*- coding:utf8 -*-
import sys     
reload(sys)    
sys.setdefaultencoding('utf8')    

import json
import urllib
import MySQLdb
import types

# 打开数据库连接
db = MySQLdb.connect("localhost","root","eas140900","warframe" ,charset='utf8')

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

file = open("zh_name2.txt")

transDict = {}

def uploadDBbyName(name,name_zh):
    # SQL 插入语句
    sql = """UPDATE item set name_zh= '%s'    where name_en = '%s' """%(name_zh,name )
    try:
         # 执行sql语句
         cursor.execute(sql)
         # 提交到数据库执行
         db.commit()
         return True
    except:
         # Rollback in case there is any error
         db.rollback()
         return False

def uploadDBbyId(id,name_zh):
    # SQL 插入语句
    sql = """UPDATE item set name_zh= '%s'    where id = '%s' """%(name_zh,id )
    try:
         # 执行sql语句
         cursor.execute(sql)
         # 提交到数据库执行
         db.commit()
         return True
    except:
         # Rollback in case there is any error
         db.rollback()
         return False


def trans(nameEn):
    words = nameEn.split(' ')
    lens = len(words)
    resZh = ""
    startIndex = 0
    while(startIndex < lens):
        #单词有直接翻译，就翻译
        nowWord = ""
        for endIndex in range(startIndex,lens):
            #组合成新的分词
            nowWord += words[endIndex]
            #print nowWord
            #check
            zhWord = transDict.get(nowWord)
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

def getInfo():
    db = MySQLdb.connect("localhost","root","eas140900","warframe",charset='utf8' )

    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    sql = """SELECT id,name_en from item where name_zh is null """  
        # 执行SQL语句
    cursor.execute(sql)
    # 获取所有记录列表
    results = cursor.fetchall()
    resStr = ""
    for row in results:
        id=row[0]
        nameEn=row[1]
        ##print nameEn+" = "+trans(nameEn)
        #continue
        if not uploadDBbyId(id,trans(nameEn)):
            print nameEn+" = "+trans(nameEn)
        
    # 打印结果
    return resStr

line = file.readline()
while line:
    line = file.readline()
    l = line.split('\t')
    if(len(l)<2):
            continue
    lt = l[1].split('\n')
    l[1] = lt[0]
    transDict[l[0]] = l[1]
    if not line:
            break
    pass # do something
getInfo()
#print trans(sys.argv[1])






