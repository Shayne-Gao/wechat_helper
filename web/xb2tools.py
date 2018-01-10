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
import sys
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')


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
    for cb,info in resultMap.items():
        resStr += '<br> <b>%s</b> <br>'%cb
        resStr += '<ul>'
        for i in info:
            if '*' in i :
                i = i.replace('*','')
                resStr +=  '<li><b>'+i+'</b></li>'
            else:
                resStr +=  '<li>'+i+'</li>'
        resStr += '</ul>'
    resStr += "<img src='%s'>"%('http://img3.dwstatic.com/tv/1712/376334745641/1512557208462.jpg')
    context['res'] = resStr
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
