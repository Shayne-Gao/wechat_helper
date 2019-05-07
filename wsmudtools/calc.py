#!/usr/bin/python
# -*- coding:utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import urllib
import MySQLdb
import types
import time
import datetime
class WsmudCalc:   
    def dazuo(self,neiliPerSec,neiliNow,neiliTarget):
        return (neiliTarget - neiliNow) / ( neiliPerSec * 6 ) #min

    def qianneng(self,level,begin,end,bornwx=0,afterwx=0,learnRate=0,prcRate=0):
        levelRate = {};
        ret = {};
        levelRate['白']=1
        levelRate['绿']=2
        levelRate['蓝']=3
        levelRate['黄']=4
        levelRate['紫']=5
        levelRate['橙']=6
        needQN = (begin + end) * (end - begin) *5 * levelRate[level] / 2
        ret['needQN'] = needQN
        ret['needMoney'] = str( needQN /5 /100 )+"金"+ str(needQN /5%100) + "银"
        if bornwx==0 and afterwx ==0:
            return ret
        else:
            #计算训练和学习的时间
            #训练  每一跳的消耗公式＝（先天悟性＋后天悟性）×（1＋练习效率%－先天悟性%）
            ret['prcPerHit'] = (bornwx + afterwx ) * ( 1.0 + prcRate / 100.0 - bornwx / 100.0 )
            ret['prcTime'] = round(needQN / ret['prcPerHit'] / 12         ,2)
            #学习  每一跳的消耗公式＝（先天悟性＋后天悟性）×（1＋学习效率%－先天悟性%）×3
            ret['learnPerHit'] = (bornwx + afterwx ) * ( 1.0 + learnRate / 100.0   ) * 3.0 
            ret['learnTime'] = round(needQN / ret['learnPerHit'] / 12         ,2)
            return ret


#print WsmudCalc().dazuo(9,6191,10000)
#print WsmudCalc().qianneng('绿',186,300,22,36,110,30);
#wm = WmPricer()
#print WmPricer().getPriceSimpleStatistic('Ash Prime Set', 3*24*3600)
