# ecoding:utf-8
from __future__ import unicode_literals
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import time
import random
import re
import urllib  
import HTMLParser  
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')
import json

from xb2.combo_tool import ComboTool
 


def index(request):
    context          = {}
    context['alarm'] = warframe().getAlarm()
    context['invasion']= warframe().getInvasion()
    context['sorties'] = warframe().getSorties()
    return render(request, 'index.html', context)

def xb2_combo(request):
    bladeInfo =     ComboTool().read_blade_cfg()
    context = {}
    context['blade_info'] = bladeInfo
    return render(request,'xb2_combo.html',context)

def combo_result(request):
    
    req =request.GET['req']
    reqLine = req.split('\r\n')
    resultContent = ''
    master = {}
    for line in reqLine:
        if '=' not in line:
            continue
        line = line.replace('\n','').replace('\r','').strip()
        masterName,blades = line.split('=',2)
        master[masterName] = blades.split(' ')
    context = {}
    resultMap =  ComboTool().getCombo(master)
    resStr = ''
    eleList = ComboTool().eleColorMap
    outputCount = 0;
    resList = []
    for ele in eleList:
        for cb,info in resultMap.items():
            if cb[4] != ele.decode('utf-8'): continue
            #插入表头
            headList = [True] #表明是表头
            tempList = []
            for e in cb.split('-'):
                tempList.append(e)    
            headList.append(tempList)
            #插入最后一个元素的颜色作为表头颜色
            headList.append(eleList[cb[4].encode('utf-8')])
            resList.append(headList)
            #插入内容
            cbList = [False] #表明是内容
            tempList = []
            for i in info:
                tempList.append(i)
            cbList.append(tempList)
            resList.append(cbList)

    resStr += "<img src='%s'>"%('http://img3.dwstatic.com/tv/1712/376334745641/1512557208462.jpg')
    context['res'] = resStr
    context['combo'] = resList
    context['debug'] = json.dumps(resList,encoding='UTF-8',ensure_ascii=False)
    return render(request, 'xb2_combo_result.html', context)

def build(request):
    context = {}
    res = warframe().getBuildlikeName( request.GET['item'])
    html_parser = HTMLParser.HTMLParser()
    res = html_parser.unescape(res)
#    res   = HTMLParser().unescape(res)
    context['res'] = res
    print res
    return render(request, 'result.html', context)


