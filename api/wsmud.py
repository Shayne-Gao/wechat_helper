# ecoding:utf-8


from __future__ import unicode_literals
import sys
sys.path.append("/root/python_util")
reload(sys)
sys.setdefaultencoding('utf-8')
import MyUtil as Util

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import urllib  
import HTMLParser  
from actbook.statistic import *
from actbook.db import *
from actbook.category import *
from actbook.analysis import *
from actbook.record import AccountRecord
# APP_ID = 你的app id
# APP_SECRET = 你的app secret


# 实例化 WechatBasic
 
MAX_RECORD_LIMIT =1000

@csrf_exempt
def post_record(request):
    print 'ho'
    #post like  @js $.post("http://119.29.138.20/api/wsmud_recordd", { role_name: "unkonw", role_menpai: "(menpai)" ,state:"(state)",last_state:"(last_state)",hp:"(:hp)",maxhp:"(:maxHp)",mp:"(:mp)",maxMp:"(:maxMap)",has_success_buff:"(hasSuccess)",pot:"(pot)",isalive:"(:alive)",iscombating:"(:combating)"})
    data=request.POST
    if data['role_menpai'] == '无门无派':
        return JsonResponse({'res': 'Empty data'})
    print data
    res = Util.dict2mysql('life','wsmud_record',data)
    print res
    return JsonResponse({'res': 'Success'})
