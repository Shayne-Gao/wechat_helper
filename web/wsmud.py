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

from wsmudtools.db import WsmudDB
 

def status(request):
    ids = []
    skipid=''
    if 'id' in request.GET:
        tmap = {}
        tmap['role_id'] = request.GET['id']
        ids.append(tmap)
    else:
        ids = WsmudDB().getAllRoldId()
        skipid='ovqq3e458b1'
    resCombine = []
    for acc in ids:
        if acc['role_id'] == skipid:
            continue 
        resr=WsmudDB().getRecentRecord(acc['role_id'])
        if len(resr) > 0:
            role = resr[0]
            s={}
            passTime = int(time.time() -   time.mktime(role['create_time'].timetuple()))
            if passTime > 600:
                passTime = 'Expire'
            s['rtime'] = passTime
            s['menpai'] =str( role['role_menpai'])[0:6]
            s['state'] = role['state']
            retStr = ''
            if role['has_success_buff'] == 'true':
                retStr += "鼓舞 "
            if role['isalive'] == 'false':
                retStr += "死亡 "
            if role['iscombating'] == 'true':
                retStr += "战斗中"
            if retStr == '':
                retStr = '无Buff'
            s['ext_state'] = retStr
            s['pot'] = role['pot']
            if True or 't' in request.GET and request.GET['t'] =='full':
                s['text'] = role['recent_text'].replace('br','\n')
            else:
                text = role['recent_text'].split('br')
                s['text'] = text[-3]+"\n"+text[-2]
            #颜色处理
            if s['rtime'] == 'Expire':
                s['bgcolor'] = 'b3b3b3'
            elif '鼓舞' in  s['ext_state'] :
                s['bgcolor'] = '#ffff4d'
            elif s['state'] in ['打坐','学习','练习']:
                s['bgcolor'] = '#809fff'
            elif s['state'] in '挖矿,炼药':
                s['bgcolor'] = '#d9b38c'
        resCombine.append(s)
    
    content={}
    content['status'] = resCombine
    return render(request,'wsmud_status.html',content)

