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
# APP_ID = 你的app id
# APP_SECRET = 你的app secret


# 实例化 WechatBasic
 
MAX_RECORD_LIMIT =1000

@csrf_exempt
def sendMail(request):
    print 'ho'
    #post like  @js $.post("http://119.29.138.20/api/wsmud_recordd", { role_name: "unkonw", role_menpai: "(menpai)" ,state:"(state)",last_state:"(last_state)",hp:"(:hp)",maxhp:"(:maxHp)",mp:"(:mp)",maxMp:"(:maxMap)",has_success_buff:"(hasSuccess)",pot:"(pot)",isalive:"(:alive)",iscombating:"(:combating)"})
    data=request.GET
    target_mail_address=['520036004@qq.com']#'341061229@qq.com'];
    #文件正文
    if 'title' not in data:
        return JsonResponse({'res': 'Fail!Empty Title!'})    
    if 'body' in data:
        body=data['body']
    else:
        body='空白内容';
    dataStr= '''<html>
<body>
<p></p>
<table>
<tr>
<th>Person</th><th>Day</th><th>Month</th><th>Year</th>
</tr>
<tr>
<td>Joe</td><td>3rd</td><td>August</td><td>1970</td>
</tr>
<tr>
<td>Sally</td><td>17th</td><td>August</td><td>1973</td>
</tr>
</table>
<a src="wsmud.com">SRC</a>

https://pushbear.ftqq.com/admin/#/channel/send/13473

<span lang=EN-US><a href="https://pushbear.ftqq.com/admin/#/channel/send/13473">https://pushbear.ftqq.com/admin/#/channel/send/13473</a><o:p></o:p></span>
<img loading="lazy" src="//cdn.v2ex.com/gravatar/862c28e4bdd958dd59f524b8df04b56e?s=73&amp;d=retro" class="avatar" border="0" align="default">
</body>
</html>
''';
    title=data['title']
    dataStr = body
    res=Util.send_mail(target_mail_address,title,dataStr);
    print res

    return JsonResponse({'res': 'Success'})

t=["520036004@qq.com"]
title='今日帮派站提醒'
dataStr='不是垃圾邮件不是的!!'
#print Util.send_mail(t,title,dataStr);
#print t
