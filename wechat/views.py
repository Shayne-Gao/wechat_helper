 	# ecoding:utf-8
from __future__ import unicode_literals
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk.basic import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
from warframe import warframe
import time

WECHAT_TOKEN = "J29djw0OwplP"
# APP_ID = 你的app id
# APP_SECRET = 你的app secret


# 实例化 WechatBasic
wechat_instance = WechatBasic(token=WECHAT_TOKEN)


@csrf_exempt
def index(request):
    if request.method == 'GET':
        # 检验合法性
        # 从 request 中提取基本信息 (signature, timestamp, nonce, xml)
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')

        if not wechat_instance.check_signature(
                signature=signature, timestamp=timestamp, nonce=nonce):
            return HttpResponseBadRequest('Verify Failed')

        return HttpResponse(
            request.GET.get('echostr', ''), content_type="text/plain")

    # 解析本次请求的 XML 数据
    try:
        wechat_instance.parse_data(data=request.body)
    except ParseError:
        return HttpResponseBadRequest('Invalid XML Data')

    # 获取解析好的微信请求信息
    message = wechat_instance.get_message()

    # 关注事件的默认回复
    response = wechat_instance.response_text(
        content=(
            '感谢您的关注！这里将会偶尔更新一些有趣的内容，并且逐渐提供一些新奇的小功能哦！\n回复【help】查看支持的功能'
            ))

    if isinstance(message, TextMessage):
        # 当前会话内容
        startTime = time.time()
        content = message.content.strip()
        reply_text = '没有找到您的命令，再试试哦'
        if content == 'help':
            reply_text = (
                    '目前支持的功能(不用输出括号！)：\n1. 输入【博客】来查看我的博客\n'
                    '2. 回复【wf 物品名或部分物品名】\n    来查询warframe国际版的物品价格，支持模糊查询和英文。 例如【wf rhino】\n'
                    '3. 回复【wf 警报】或者【wf alarm】\n    来查询warframe国际版的警报任务\n'
                    '4. 回复【wfb 战甲或者武器名】\n    来查询其推荐的Mod配置，支持模糊查询和英文。例如【wf 关刀】\n'
                    '5. 直接回复来上报bug和提出建议\n\n'
                    '还有更多功能正在开发中哦 ^_^\n'
                    '--------臭不要脸的分割线---------\n'
                    '本服务无广告，永久免费使用，如果想要鼓励程序猿小哥哥开发更多功能，欢迎点击 【<a href="http://ww3.sinaimg.cn/large/0060lm7Tly1fja0i4bndpj308e090gnv.jpg">微信二维码</a>】喂食！五毛不嫌多，一块不嫌少！'
                )
        elif content == '博客':
            reply_text = '【<a href="http://weibo.com/u/1628831502?refer_flag=1001030001_&nick=%E5%A2%A8%E5%8C%BF%E7%BB%87%E4%BA%A4">我的围脖</a>】'+'【<a href="http://hi-ink.lofter.com/">我的摄影空间</a>】'
        elif content == '随机111':
            reply_text = '随机功能还在开发中噢,亲可以先查看【<a href="http://www.ddhbblog.sinaapp.com">我的博客</a>】'
        elif content == '小绿':
	        reply_text = '么么哒恭喜你进入了隐藏的空间，当你看到这句话的时候我一定在想你哟！'
        elif content.startswith('wfb'):
            wf = warframe()
            subContent = content[3:].strip()
            if subContent[-1].lower() =='p':
                reply_text = wf.getBuildlikeName(subContent[0:-1])
            else:
                reply_text = wf.getBuildlikeName(subContent)
        elif content.startswith('wf'):
            wf = warframe()
            subContent = content[2:].strip()
            if subContent =='警报' or subContent.lower()=='alarm':
                reply_text = wf.getAlarm()
            else:
                #subContent = subContent.replace('prime','')
                #兼容最后的p，比如犀牛p
                if subContent[-1].lower() =='p':
                    reply_text = wf.getInfoByName(subContent[0:-1])
                else:
	    	        reply_text = wf.getInfoByName(subContent)
        elif content == '喂食':
            reply_text ="本服务无广告，永久免费使用，如果想要鼓励程序猿小哥哥开发更多功能，欢迎点击 【<a href='http://ww3.sinaimg.cn/large/0060lm7Tly1fja0i4bndpj308e090gnv.jpg'>微信二维码</a>】喂食！五毛不嫌多，一块不嫌少！"
    	else:
        	reply_text = '功能还在开发中哦,亲可以提出您宝贵的意见'
        processTime = time.time() - startTime
        if len(reply_text)<40 :
            status='ERRE'
        elif processTime >4.5:
            status='EXPI'
        else:
            status='SUCC'
        logTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print "[AccessLog][%s][%s][Time:%s][RespLen:%s][Req:%s]"%(logTime,status,processTime,str(len(reply_text)),content)
        print "Response:"+reply_text
        response = wechat_instance.response_text(content=reply_text)

    return HttpResponse(response, content_type="application/xml")
