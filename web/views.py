# ecoding:utf-8
from __future__ import unicode_literals
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from warframe import warframe
import time
import random
import re
from random import choice
 
# APP_ID = 你的app id
# APP_SECRET = 你的app secret


# 实例化 WechatBasic
 


@csrf_exempt
def index(request):
    # if request.method == 'GET':
    reply_text = "<pre>" 
    #reply_text += warframe().getPriceList('123')
    reply_text += warframe().getAlarm()
    reply_text +="</pre>"
    return HttpResponse(reply_text)
