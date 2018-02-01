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
def sbn_tool(request):
    context = {}
    #return render(request,'sbn_tool.html',context)
    return render(request,'test.html',context)

def price_searcher(request):
    if len(request.GET) == 0 :
        return render(request, 'price_searcher.html')
    key = '' if 'item' not in request.GET else  request.GET['item']
    context  = {}
    context['faxian'] = LifeTool().getItemPrice(key)
    return render(request, 'price_searcher.html', context)

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
