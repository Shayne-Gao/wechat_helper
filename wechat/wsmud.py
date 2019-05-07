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
import datetime
#from wsmud.calc import WsmudCalc

from wsmudtools.calc import WsmudCalc
from wsmudtools.db import WsmudDB
class wsmud():
    def status(self):
        retStr = ''
        res = WsmudDB().getAllRoldId()
        for acc in res: 
            resr=WsmudDB().getRecentRecord(acc['role_id'])
            print resr
            role = resr[0]
            passTime = int(time.time() -   time.mktime(role['create_time'].timetuple()))
            if passTime > 600:
                passTime = 'Expire'
            retStr += role['role_menpai']+"<"+role['state']+"> "
            if role['has_success_buff'] == 'true':
                 retStr += "鼓舞 "
            if role['isalive'] == 'false':
                retStr += "死亡 "
            if role['iscombating'] == 'true':
                retStr += "战斗中"
            retStr += "("+ str(passTime)+"s)\n"
            #retStr += "之前:"+"<"+role['last_state']+">\n"
            retStr += "潜能:" + role['pot'] +"\n"
            retStr += role['recent_text'].replace("br","\n")
            #retStr += "气血:"+ role['hp'] + "/" + role['maxhp']+"  内力:"+ role['mp'] + "/" + role['maxmp']+"\n"
            #retStr += "记录时间:" + str(role['create_time']) + "\n"
            retStr += '--------------\n'
        return retStr

    def qianneng(self,inputline):
#evel,begin,end,bornwx=0,afterwx=0,prcRate=0,learnRate=0
        inlist=inputline.strip().split(' ')
        i=0
        for k in inlist:
            if i>2:
                inlist[i] = int(k)
            i = i+1

        text = ''
        if len(inlist)==4:
            res= WsmudCalc().qianneng(inlist[1],int(inlist[2]),int(inlist[3]))
            for k,v in res.items():
                res[k] = str(v)
            text='需要潜能：' + res['needQN'] + '\n'
            text+='需要金币：' + res['needMoney'] + '\n'
        elif len(inlist)==8:
            res =  WsmudCalc().qianneng(inlist[1],int(inlist[2]),int(inlist[3]),inlist[4],inlist[5],inlist[6],inlist[7])
            for k,v in res.items():
                res[k] = str(v)
            text='需要潜能：' + res['needQN'] + '\n'
            
            text += '练习所需时间：'+wsmud().min2hour(res['prcTime']) +'\n（'+ res['prcPerHit'] +'每跳消耗潜能）\n'
            text += '学习所需时间：'+wsmud().min2hour(res['learnTime']) +'\n（'+ res['learnPerHit'] +'每跳消耗潜能）\n'
            text += '----------------------------回复qn查看用法\n'
        elif len(inlist) <4:
            text += '用法：qn 技能颜色 当期等级 目标等级 先天悟性 后天悟性 学习效率 练习效率\n'
            text += '用法：qn 技能颜色 当期等级 目标等级 \n'
    
            text += '例:qn 绿 0 300 30 107 50 80\n'
        return str(text)

    def min2hour(self,floatMin):
        floatMin = float(floatMin)
        if floatMin <= 60:
            return str(floatMin)+"分钟"
        else:
            h=int(floatMin/60)
            m=floatMin%60
            return str(h)+"小时"+str(m)+"分钟"

#print wsmud().status()
