#!/usr/bin/python
# -*- coding:utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ItemNickName:

    nickname = {
'鱼骨':'螺钉步枪',
'喷火器':'伊格尼斯',
'rhnio':'rhino',
'女汉子':'valkyr',
'瓦喵':'valkyr',
'李明博':'Limbo',
'龙甲':'Chroma',
'集团鞭':'Secura Lecta',
'刷钱鞭':'Secura Lecta',
'钱鞭':'Secura Lecta',
'诺娃':'nova',
'集团海克':'Vaykor Hek',
'圣剑':'Excalibur',
'g鞭':'阿特拉克斯',
'奥提克':'Opticor',
'矿枪':'quanta',
'莲花':'破坏者',
'o炮':'Opticor',
'手弩':'Ballistica',
'血摸':'Nekros',
'保障 勒克塔':'Secura Lecta',
'音乐甲':'Octavia',
'暴击鞭':'Atterax',
'沙甲':'atlas',
'猴子':'wukong',
'主教':'harrow',
'工程师':'vauban',
'布利斯提卡':'Ballistica',
'亡魂喷火器':'伊格尼斯',
'伊格尼斯亡魂':'伊格尼斯 亡魂',
'布里斯提卡':'Ballistica',
'':'',
'':'',
'':'',
'':'',
'':'',
'':'',
'':'',
'':'',
    }
    
    def get(self,name):
        name = name.lower()
        name = name.encode("utf-8")  
        if self.nickname.get(name) is not None:
            return self.nickname[name]
        else:
            return name
