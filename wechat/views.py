 	# ecoding:utf-8
from __future__ import unicode_literals
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk.basic import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
from warframe import warframe
from life import life
from accountbook import AccountBook
import time
import random
import re
from random import choice
import datetime
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
        content = content.encode("utf-8")  
        reply_text = '没有找到您的命令，再试试哦\n'
        #-------------------------------------------------------------------------------------------------------
        #以下为基础帮助等功能
        if content.lower() == 'help':
            reply_text = (
                    '目前支持的功能(不用输出括号！)：\n1. 输入【博客】来查看我的博客\n'
                    '2. 回复【wf 物品名或部分物品名】\n    来查询warframe国际版的物品价格，支持模糊查询和英文。 例如【wf rhino】\n'
                    '3. 回复【警报】或者【wfa】\n    来查询warframe国际版的警报任务\n'
                    '4. 回复【wfb 战甲或者武器名】\n    来查询其推荐的Mod配置，支持模糊查询和英文。例如【wfb 关刀】\n'
                    '5. 回复【调教+内容】上报bug和提出建议\n'
                    '6. 点击【<a href="http://bbs.ngacn.cc/read.php?tid=12377993">查看版权和更新等信息</a>】\n\n'
                    '还有更多功能正在开发中哦 ^_^\n'
                    '--------臭不要脸的分割线---------\n'
                    '本服务无广告，永久免费使用，如果想要鼓励程序猿小哥哥开发更多功能，欢迎点击 【<a href="http://ww3.sinaimg.cn/large/0060lm7Tly1fja0i4bndpj308e090gnv.jpg">微信二维码</a>】喂食！五毛不嫌多，一块不嫌少！\n'
                )
        elif content == '博客':
            reply_text = '【<a href="http://weibo.com/u/1628831502?refer_flag=1001030001_&nick=%E5%A2%A8%E5%8C%BF%E7%BB%87%E4%BA%A4">我的围脖</a>】'+'【<a href="http://hi-ink.lofter.com/">我的摄影空间</a>】\n'
        elif content == '说明':
            reply_text = (
                    '版权说明：warframe相关的价格信息来自warframe.market,build信息来自于warframe-build.com。 翻译词库来源于网友\n'
                    '本公众号非商业化，功能全部免费\n'
                )
        elif content.startswith('调教'):
            reply_text = ('感谢您的反馈！每一条都会被记录下来，会尽量回复的哦！\n\r')
        elif content == '小绿':
	        reply_text = '么么哒恭喜你进入了隐藏的空间，当你看到这句话的时候我一定在想你哟！\n'
        elif content == '喂食':
            reply_text ="本服务无广告，永久免费使用，如果想要鼓励程序猿小哥哥开发更多功能，欢迎点击 【<a href='http://ww3.sinaimg.cn/large/0060lm7Tly1fja0i4bndpj308e090gnv.jpg'>微信二维码</a>】喂食！五毛不嫌多，一块不嫌少！"

        #-------------------------------------------------------------------------------------------------------
        #以下为warframe功能的识别
        elif content.lower().startswith('wfb'):
            wf = warframe()
            subContent = content[3:].strip()
            if subContent.startswith('亡魂'):
                subContent = subContent.replace('亡魂','')
                subContent = subContent + ' 亡魂'
            if subContent[-1].lower() =='p':
                reply_text = wf.getBuildlikeName(subContent[0:-1])
            else:
                reply_text = wf.getBuildlikeName(subContent)
        elif content.lower().startswith('wf '):
            wf = warframe()
            subContent = content[2:].strip()
            if subContent =='警报' or subContent.lower()=='alarm':
                reply_text = wf.getAlarm()
            else:
                #subContent = subContent.replace('prime','')
                #处理亡魂
                if subContent.startswith('亡魂'):
                    subContent = subContent.replace('亡魂','')
                    subContent = subContent + ' 亡魂'
                #兼容最后的p，比如犀牛p
                if subContent[-1].lower() =='p':
                    reply_text = wf.getInfoByName(subContent[0:-1])
                else:
	    	        reply_text = wf.getInfoByName(subContent)
        elif content.lower()=='wfa' or content=='警报':
            reply_text = warframe().getAlarm()
        elif content=='入侵':
            reply_text = warframe().getInvasion()
        elif content=='突击':
            reply_text = warframe().getSorties()
        # elif content.lower()=='list':
        #     reply_text = warframe().getPriceList(wechat_instance.message.source)

          #-------------------------------------------------------------------------------------------------------
        #以下为其他生活功能的识别
        elif content.lower().startswith('s'):
            req = content.replace('s','')
            reply_text = life().scarf(int(req))
        elif content.lower().startswith('k'):
            inputStr = content[1:]
            if '=' in inputStr:
                inputList = inputStr.split('=')
                setRes = life().setKV(inputList[0],inputList[1])
                reply_text = '已经将%s设置为%s'%(inputList[0],inputList[1]) if setRes else 'Set Fail'
            else:
                getRes = life().getKV(inputStr)
                reply_text ='【%s】的查询结果:\r\n%s'%(inputStr,getRes) if getRes is not False else 'Get Fail'
        elif content.startswith( '班车'):
            reply_text = "19:00\n19:10\n19:30\n19:45\n20:00\n20:10\n20:30\n21:05\n21:30\n22:10\n"
        #-------------------------------------------------------------------------------------------------------
        #以下为记账功能的识别
        elif hasUserPremission(wechat_instance.message.source,'actbook'): 
            if  re.match('^\d', content) :
                res = AccountBook().insertAccountRequest(content)
                reply_text = res
            elif content.startswith('明细'):
                yearMonth = content.replace('明细','')
                if yearMonth == '':
                    year = datetime.date.today().year
                    month = datetime.date.today().month
                    page=1
                else:
                    year = yearMonth[0:2]
                    month = yearMonth[2:4]
                    page = yearMonth[4:5] if len(yearMonth)==5 else 1
                    year = '20'+year
                reply_text = AccountBook().getRecordByYearMonth(year,month,'id desc',int(page))
            elif content.startswith('统计'):
                yearMonth = content.replace('统计','')
                if yearMonth == '':
                    year = datetime.date.today().year
                    month = datetime.date.today().month
                    page =1
                else:
                    year = yearMonth[0:2]
                    month = yearMonth[2:4]
                    page = yearMonth[4:5] if len(yearMonth)==5 else 1
                    year = '20'+year
                reply_text = AccountBook().getAnalysisByYearMonthAndRecord(year,month,page)
            elif content.startswith('分类'):
                yearMonth = content.replace('分类','')
                if yearMonth == '':
                    year = datetime.date.today().year
                    month = datetime.date.today().month
                else:
                    year = yearMonth[0:2]
                    month = yearMonth[2:4]
                    year = '20'+year
                reply_text = AccountBook().getAnalysisByYearMonth(year,month)
            elif content == '撤销':
                #uid暂时传个1
                delRes = AccountBook().deleteLatestRecord(1)
                reply_text = delRes
            elif content.startswith('归类'):
                newType = content.replace('归类','');
                classfyRes = AccountBook().classifyLastRecord(1,newType)
                reply_text = classfyRes
                
    	else:
        	reply_text = '未找到该命令，是不是忘了加wf和空格？输入help查看功能哦\n'


        #-------------------------------------------------------------------------------------------------------

        processTime = time.time() - startTime
        if len(reply_text)<100 :
            status='\033[1;33mERRE\033[0m'
        elif processTime >4.8:
            status='\033[1;31mEXPI\033[0m'
        else:
            status='SUCC'
        logTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print "[AccessLog][%s][%s][Time:%s][RespLen:%s][Req:%s][from:%s][to:%s]\n"%(logTime,status,processTime,str(len(reply_text)),content,wechat_instance.message.source,wechat_instance.message.target)
        print "\nResponse:"+reply_text
        #在这里加入通知
        if content.startswith('wf'):
            reply_text+=getFooter()
        response = wechat_instance.response_text(content=reply_text)

    return HttpResponse(response, content_type="application/xml")

def hasUserPremission(wechatId, permissionType):
   
    if permissionType == 'actbook':
        actbook = ['opD4r0WskoVJmlirA9ubVCVpg-k0']
        if wechatId in actbook:
            return True
        else:
            return  False

#随机获取页尾进行展示
def getFooter():
    showRate = 10 #10为100%展示
    if random.randint(1, 10) >= showRate:
        return ''
    str = '【小尾巴】'
    foot = [
        '你知道吗？回复 调教+内容就可以上报各种问题了！',
        '点击<a href="http://bbs.ngacn.cc/read.php?tid=12377993">查看版权更新等信息</a>哦',
        '有命令忘记了？输入help来查看！',
        '回复 喂食 来为公众号开发出一份力！',
        '复制这句话，打开支付宝领取大大大红包！&C5RhvX810X&  '
        '有时候提示错误了请不要急，多给程序娘一点时间稍后再试',
        '个人公众号无法主动推送任何消息哦',
        '现在输入wfa或者警报 就可以查询警报啦',
    ]
    str += choice(foot)+"\n"
    return str

#print  AccountBook().getAnalysisByYearMonthAndRecord(2017,10)
#print getFooter()
#print hasUserPremission('opD4r0WskoVJmlirA9ubVCVpg-k0','actbook')
