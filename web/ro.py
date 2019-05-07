# ecoding:utf-8
from __future__ import unicode_literals
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
def index(request):
    if len(request.GET) == 0 or 'begin' not in request.GET:
        #初始化时间控件
        context = {}
        begin  = time.strftime("%Y-%m-01")
        thisMonth = time.strftime("%m")
        nextMont =( int(thisMonth) +1) % 12
        if nextMont < 10:
            nextMont = '0'+str(nextMont)
        end = time.strftime("%%Y-%s-01"%(nextMont))
        return render(request, 'ro.html',context)


    else:
        begin = request.GET['begin']
        end = request.GET['end']
    startStamp = time.mktime(time.strptime(begin,"%Y-%m-%d"))
    endStamp = time.mktime(time.strptime(end,"%Y-%m-%d"))
    #拼接数据order by
    if 'q' not in request.GET or request.GET['q']=='':
        orderby='create_time desc'
    else:
        orderby=request.GET['q']+' desc'
    #获取详细数据
    res = AccountBookDB().getAllRecordByTime(startStamp,endStamp,MAX_RECORD_LIMIT,orderby);
    context = {}
    context['actRec'] = []
    context['begin'] = begin
    context['end'] = end
    costSum = 0;
    num = 0
    for record in res:
        if len(record) < 6:
            continue
        actRec = {}
        actRec['recordId'] = record[0]
        actRec['userId'] = record[1]
        actRec['cost'] = record[2]
        actRec['type'] = record[3]
        actRec['cateId'] = record[4]
        actRec['cateText'] = Category().getCategoryNameById(actRec['cateId'])
        actRec['content'] = record[5]
        actRec['createTime'] = record[6].strftime('%m-%d')
        #背景色
        if num % 2 ==0:
            actRec['bgcolor'] = '#a4c2f4'
        num += 1
        context['actRec'].append(actRec)
        costSum +=  actRec['cost']
        actRec['cost'] = "%.02f"%(actRec['cost'])
    context['cost_sum'] = costSum
    #获取分类信息

    res =  Analysis().getPercent(int(startStamp),int(endStamp),MAX_RECORD_LIMIT)
    cateList = []
    responseStr = ''
    if len(res)!=0:
        for r in res:
            markNum = int(float( r['percent'])) / 1+1
            mark = '';
            for i in range(0,markNum):
                mark += "|"
            cateList.append(r)
        #获取其他没记录的分类列表
        context['cate_info'] = cateList
    
    #获取所有分类信息展示下拉菜单
    context['allcate_info'] =  Category().getAllCategoryGroupById()
    return render(request, 'accountbook.html', context)

def modifyRecordType(request):
    uid = 1
    if 'type_name' not in request.GET or 'rid' not in request.GET:
        return JsonResponse({'res': 'invalid paras'})
    typeName = request.GET['type_name']
    rid= request.GET['rid']
    AccountRecord().classifyRecordType(uid,rid,typeName)
    return JsonResponse({'res': 'Success'})
