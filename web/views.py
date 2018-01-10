# ecoding:utf-8
from __future__ import unicode_literals
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from warframe import warframe
import time
import random
import re
from random import choice
import urllib  
import HTMLParser  
from life import LifeTool
# APP_ID = 你的app id
# APP_SECRET = 你的app secret


# 实例化 WechatBasic
 


@csrf_exempt
def index(request):
    context          = {}
    context['alarm'] = warframe().getAlarm()
    context['invasion']= warframe().getInvasion()
    context['sorties'] = warframe().getSorties()
    return render(request, 'index.html', context)

def priceList(request):
    requestType = request.GET['type']
    reply_text = "<pre>"
    reply_text += warframe().getPriceList(requestType)
    reply_text += warframe().getAlarm()
    reply_text +="</pre>"
    return HttpResponse(reply_text)
    context = {}
    context['res'] =reply_text
    return render(request, 'result.html', context)

def price(request):
    context = {}
    res ="<tr><td>类型</td><td>物品</td><td>英文名</td><td>最低售价</td><td>详情</td><td>记录时间</td><td>卖家</td><tr>"
    res += warframe().getInfoByName( request.GET['item'],True)
    context['res'] = res
    return render(request, 'result.html', context)
def sbn_tool(request):
    context = {}
    #return render(request,'sbn_tool.html',context)
    return render(request,'index.html',context)

def sbn_result(request):
    
    req =request.GET['req']
    reqLine = req.split('\r\n')
    resultContent = ''
    title = LifeTool().getSBNTitle()
    resultContent += title.replace('\n','<br>')
    for r in reqLine:
        singleParam = r.split(',')
        if len(r) == 0 :
            continue
    #    resultContent = singleParam
        resultContent+=  LifeTool().getSBNContent(str(singleParam[0]),str(singleParam[1]),int(singleParam[2]),int(singleParam[3])).replace('\n','<br>')
    context = {}
    context['res'] = resultContent
    return render(request, 'result.html', context)

def build(request):
    context = {}
    res = warframe().getBuildlikeName( request.GET['item'])
    html_parser = HTMLParser.HTMLParser()
    res = html_parser.unescape(res)
#    res   = HTMLParser().unescape(res)
    context['res'] = res
    print res
    return render(request, 'result.html', context)
