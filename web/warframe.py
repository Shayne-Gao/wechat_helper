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
from wftools.translator import WmTranslator
from wftools.pricer import WmPricer
from wftools.builder import WmBuilder
from wftools.ItemNickName import ItemNickName
from wftools.alarm import WmAlarm
from wftools.itemUtil import ItemUtil
class warframe(object):
    MAX_RECORD_NUM = 5 
    #MAX_RECORD_PRICE_NUM = 1 #最大查询价格的物品数目
    MAX_URL_PRICE_NUM = 1 #查询物品结果数目少于等于此值时，强制查询远端实时价格
    MAX_PROCESS_TIME = 2#最大处理时间的秒
    MAX_BUILD_NUM = 7 #获取最多的build数量
    MAX_RESPONSE_LEN = 1400 #微信最大的返回字节数目

    PRICE_STATISTIC_TIME_PERIOD_DAY = 3# 显示几天内的价格趋势
    def timestamp_datetime(self,value):
        value = int(value)
        format = '%Y-%m-%d %H:%M:%S'
        #value为传入的值为时间戳(整形)，如：1332888820
        value = time.localtime(value)
        ## 经过localtime转换后变成
        ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
        # 最后再经过strftime函数转换为正常日期格式。
        dt = time.strftime(format, value)
        return dt

    def getZhWikiUrl(self,nameZh,nameEn,itemType):
        baseUrl = 'http://warframe.huijiwiki.com/wiki/'
        pageName = ""
        tempList = nameEn.split('Prime')
        baseName = tempList[0]
        #if nameZh is not None:
        #    pageName = nameZh
        #elif nameEn is not None:
        #    pageName = nameEn
        pageName = baseName
        return baseUrl+pageName
    
    def getBuildlikeName(self,itemName):
        wmb = WmBuilder()
        #尝试获取别名
        itemName = ItemNickName().get(itemName)
        nameEn,nameZh,buildDict = wmb.getBuildList(itemName,self.MAX_BUILD_NUM)
        if buildDict == None:
            return '未找到这个物品的build，请尝试修改关键词哦'
        str = "%s(%s)<br>"%(nameZh,nameEn)
        outputCount = 0
        modCount = {}
        for b in buildDict:
            #统计各个Mod出现的次数
            for modName in b['build_dict']:
                modCount[modName] = modCount.get(modName,0)+1
            if b['formas'] =='-':
                b['formas'] = 0
            if outputCount > self.MAX_BUILD_NUM:
                break;
            outputCount +=1
            str += '------------------------<br>'
            str += "【方案%s】【极化:%s】%s<br>"%(outputCount,b['formas'],b['build_des'])
            str+=b['build']
            
            str+= "【<a href='"+b['url']+"'>详情</a>】<br>"
            #outputCount+=1
        str += "Mod出现频率:</br>"
        sortModCount = sorted(modCount.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        print sortModCount
        for k in sortModCount:
            #获取Mod图片
            modImg = ItemUtil().getItemImgByZh(k[0])
            str+="<div style='float:left;height:350px;width:200px'>"
            str+="<img style='height:300px' src='%s'>"%(modImg)
            str+="</br>%s : %s / %s<br>"%(k[0],k[1],self.MAX_BUILD_NUM)
            str+="</div>"
        return str
            
    def getInfoByName(self,itemName,isListFormat = False):
        #记录开始时间
        startProcessTime = time.time()
        resStr = ""
        #尝试获取别名
        itemName = ItemNickName().get(itemName)
        #尝试直接翻译
        trans = WmTranslator()
        directNameZh = trans.en2zh(itemName)
        if directNameZh != itemName and not isListFormat:
            resStr += "您的输入也可以直接被翻译为:"+directNameZh+"<br>"

        db = MySQLdb.connect("localhost","root","IWLX8IS12Rl","warframe",charset='utf8' )

        # 使用cursor()方法获取操作游标 
        cursor = db.cursor()
        sql = """SELECT * from item where name_zh like '%%%s%%' or lower(name_en) like '%%%s%%' ORDER BY TYPE DESC  """ %(itemName,itemName.lower())
          # 执行SQL语句
        #print sql   
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        #print results
        if len(results)==0:
            #尝试用输入找wiki
            wikiZH = self.getZhWikiUrl("",itemName,"")
            wikiZH = "【<a href='"+wikiZH+"'>Wiki</a>】"
            resStr += "未找到"+itemName+",您可以试试模糊搜索，减少搜索的字试试看.<br>也可能这个物品无法出售？用wfb来查看它的Mod配备!<br>尝试为您找到了"+wikiZH+"<br>"
            return resStr
        #这里限制长度，因为微信太长的记录显示会出错
        if len(results) > self.MAX_RECORD_NUM:
            resStr += "【提示】共搜索到%s条记录，因微信限制，只显示前%s条<br>"%(len(results),self.MAX_RECORD_NUM)
            results = results[0:self.MAX_RECORD_NUM]
        isFirst = True
        pricer = WmPricer()
        checkPrice = True
        #这里限制询价的长度，因为太多的记录询价会很慢
        listCount = 0;
        priceCount = 0;
        priceSource = ''
        if len(results) <= self.MAX_URL_PRICE_NUM:
            priceSource = 'url'
        #resStr += "<tr><td>类型</td><td>物品</td><td>英文名</td><td>Wiki</td><td>最低售价</td><td>详情</td><td>卖家</td><tr>"
        for r in results:
            resStr +="<tr>"
            name_en=r[1]
            name_zh=r[2]
            itemType = r[3]
            wikiZH = self.getZhWikiUrl(name_zh,name_en,itemType)
            wikiZH = "<a href='%s'>%s</a>"%(wikiZH,name_zh)
            resStr += "<td>%s</td><td>%s</td><td>%s</td>"%(itemType,wikiZH,name_en)
            #get price
            listCount += 1
            #如果结果集过小，强制从api获取价格
            #如果访问已经超过阈值时间，则强制从本地获取（获取不到就返回空）
            #否则走默认的方式
            nowProcessTime = time.time()
            if nowProcessTime - startProcessTime > self.MAX_PROCESS_TIME:
                priceSource = 'db'
            itemPrice = pricer.getPrice(name_en,itemType,priceSource)
            if itemPrice is not None:
                resStr += "<td>"
                resStr +="%s</td>"%(itemPrice['cheapest_price'])
                #如果采集的数据足够显示物品价格趋势，则显示近期的最高或者最低价格。否则显示前20的平均售价
                priceStat = pricer.getPriceSimpleStatistic(name_en, self.PRICE_STATISTIC_TIME_PERIOD_DAY * 24 * 3600)
                if priceStat is not None:
                    resStr += "<td>%s天内:%s-%s <br> 平均: %s"%(self.PRICE_STATISTIC_TIME_PERIOD_DAY ,priceStat['lowest'],priceStat['highest'],priceStat['avg'])
                    resStr +="<br>%s</td>"%(self.getBuySuggest(itemPrice['cheapest_price'],priceStat['lowest'],priceStat['highest'],priceStat['avg']))
                else:
                    resStr += "<td>前20平均售价：%s x %s个</td>"%(itemPrice['top_avg'],itemPrice['top_count'])
                #记录时间距离现在的时间
                if isinstance(itemPrice['record_time'],basestring):
                    timeArray = time.strptime(itemPrice['record_time'], "%Y-%m-%d %H:%M:%S")
                    timeStamp = int(time.mktime(timeArray))
                    pastTime = time.time() - timeStamp
                    pastMin = int(pastTime / 60)
                    pastSec = int(pastTime - pastMin * 60)
                    resStr +=  "<td>%s分%s秒前</td>"%(pastMin,pastSec)
                else:
                    resStr += "<td>%s分%s秒前</td>"%(itemPrice['record_time'],type(itemPrice['record_time']))
                #卖家记录
                resStr += "<td>%s</td>"%(itemPrice['top_rec'])
                pTime = time.time() - nowProcessTime
                resStr += "<td>%s-%s</td>"%(pTime,priceSource)
            else:
                resStr += "<td>未查询到售价</td>"
            resStr +="</tr>"
        return resStr
    def getBuySuggest(self,nowPrice,lowest,highest,avg):
        if nowPrice == lowest:
            return "<div  style='color: red;'><b>历史最低<b></div>"
        if nowPrice < avg*0.8:
            return "<div  style='color: orange;'><b>赶快购买<b></div>"
        elif nowPrice < avg:
            return "<div style='color:green'><b>建议购买<b></div>"
        else:
            return "观望"

    def getAlarm(self):
        str = WmAlarm().getAlarmList()
        return str     
          
    def getInvasion(self):
        return WmAlarm().getInvasionList()

    def getSorties(self):
        return WmAlarm().getSorties()
    def getPriceList(self,type):
        #get monitor item price list by user
        startTime = time.time()
        itemstobuy = [
        'Secura Lecta',
        'Energy Siphon',
        #'持久力Prime',
        '盲怒',
        '瞬时坚毅',
        '过度延展',
        '卑劣加速',
        '高压电流',
        '致命火力',
        '铝热焊弹',
        '烈焰',
        
        ]
        itemswf = [
        'Ash Prime',
        'Mag Prime',
        'Nova Prime',
        'Banshee Prime',
        'Volt Prime',
        'Oberon Prime',
        'Saryn Prime',
        'Valkyr Prime',
        'Nekros Prime',
        'Trinity Prime',
        'Rhino Prime',
        ]
        if type == 'wf':
            items = itemswf
        elif type == 'tobuy':
            items = itemstobuy
        resStr = "<table  border='3'>"
        resStr += "<tr><td>类型</td><td>物品</td><td>英文名</td><td>最低售价</td><td>详情</td><td>记录时间</td><td>卖家</td><tr>"
        count = 0
        for item in items:
            count +=1
            if count % 2 ==0:
                resStr +="<tr style='background-color:gray'>"
            else:
                resStr +="<tr>"
            resStr += self.getInfoByName(item,True)
            resStr += "</tr>"
        resStr +="</table>"
        resStr += "耗时:%s"%(time.time() - startTime)
        return resStr;
            
    

def test():
    wf = warframe()
    print wf.getBuildlikeName('鱼骨')
#------------------------------------------
#test()
#wf = warframe()
#print WmAlarm().getAlarmList()    

#print warframe().getBuildlikeName('lenz')

