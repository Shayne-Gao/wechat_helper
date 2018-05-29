# ecoding:utf-8
from __future__ import unicode_literals
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import urllib  
import HTMLParser  
from life import LifeTool
# APP_ID = 你的app id
# APP_SECRET = 你的app secret


# 实例化 WechatBasic
 


@csrf_exempt
def price_searcher(request):
    if len(request.GET) == 0 or 'item' not in request.GET:
        return render(request, 'price_searcher.html')
    key = '' if 'item' not in request.GET else  request.GET['item']
    context  = {}
    context['item'] = request.GET['item']
    print "[PriceSearcher][item=%s]"%context['item']
    context['rev'] = 0
    resList =  LifeTool().getItemPrice(key)
    if 'q' in request.GET:
        sortKey = request.GET['q']
        if 'rev' in request.GET:
            rev = True if request.GET['rev'] == '1' else False
            context['rev'] = 0 if request.GET['rev'] == '1' else 1
        else:
            rev = False
     
        sortedList =  sorted(resList,key=lambda s:s[sortKey], reverse=rev) 
        context['res'] = sortedList
    else:
        context['res'] = resList

    return render(request, 'price_searcher.html', context)
