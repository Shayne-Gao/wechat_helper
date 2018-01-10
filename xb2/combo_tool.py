#!/usr/bin/python
# -*- coding:utf-8 -*- 
import sys
sys.path.append("/root/python_util")
import Util as Util

reload(sys)
sys.setdefaultencoding('utf-8')

import requests

import time
import json
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import os
import hashlib
import pymysql
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


database_ip_and_port = 'localhost'
database_name = 'life'
database_username = 'root'
database_password = 'IWLX8IS12Rl'



blade_file_path = './blade.cfg'
master_file_path = './master.cfg'
combo_file_path = './combo.cfg'
class ComboTool:
        #定义属性对应的颜色
    eleColorMap = {'水':'#809fff',
'火':'#ff8080',
'暗':'#b3b3b3',
'地':'#d9b38c',
'雷':'#ffff4d',
'光':' #ffffe5',
'风':'#85e085',
'冰':' #e5f2ff',
}

    def read_master_cfg(self):
        file = open(os.path.dirname(os.path.realpath(__file__))+'/' + master_file_path)
        master = {}
        for line in file:
            line = line.replace('\n','').replace('\r','')
            masterName,blades = line.split('=',2)
            master[masterName] = blades.split('|')
        return master

    def read_blade_cfg(self):
        file = open(os.path.dirname(os.path.realpath(__file__))+'/' + blade_file_path)
        blade = {}
        for k,v in  self.eleColorMap.items():
            k = k.encode('utf-8')
        mapT = self.eleColorMap
        for line in file:
            line = line.replace('\n','').replace('\r','').decode('utf-8')
            info = line.split(',')
            blade[info[0]]={}
            blade[info[0]]['element'] = info[6]
            blade[info[0]]['gift'] = info[1]
            blade[info[0]]['fav1'] = info[2]
            blade[info[0]]['gender'] = info[4]
            blade[info[0]]['weapon'] = info[5]
            blade[info[0]]['fav2'] = info[3]
            blade[info[0]]['core_num'] = info[7]
            blade[info[0]]['type'] = info[8]
            blade[info[0]]['url'] = info[9]
            for k,v in  self.eleColorMap.items():
                if blade[info[0]]['element'] == k.decode('utf-8'):
                    blade[info[0]]['bgcolor'] = v
            
        return blade

    def read_combo_cfg(self):
        file = open(os.path.dirname(os.path.realpath(__file__))+'/' + combo_file_path)
        combo=[]
        for line in file:
            line = line.replace('\n','').replace('\r','').decode('utf-8')
            combo.append(line.split('|'))
        return combo

    #传入combo的三元组，还有角色的属性信息 ，查找是否有满足combo的组合
    def findCombo(self,combo,masterEle):
        result = []
        for ele in combo:
            #挨个检查三个元素的满足关系
            if ele not in masterEle:
                continue
            else:
                result.append(masterEle[ele])
        if len(result)==3: 
            returnRes = []
            #对结果进行展开，做交叉运算
            for i in result[0]:
                for j in result[1]:
                    for k in result[2]:
                        #如果发动的3个异刃不相同，则标记为推荐
                        if i != j and j != k:
                            str = "* %s -> %s -> %s"%(i,j,k)
                        else:
                            str = "%s -> %s -> %s"%(i,j,k)
                        returnRes.append( str)
            return returnRes
        else:
            return None

    def getCombo(self,masterInputMap):
        #初始化主角信息
        master = masterInputMap
        blade = self.read_blade_cfg()
        combo = self.read_combo_cfg()
#        print  json.dumps(blade, encoding='UTF-8', ensure_ascii=False)
        #获取主角所拥有异刃的属性信息
        masterInfo = {}
        for masterName,blades in master.items():
            bladeInfo = {}
            for b in blades:
                bladeInfo[b] = {}
                bladeInfo[b]['element'] = blade[b]['element']
            masterInfo[masterName] = []
            masterInfo[masterName].append(bladeInfo)
        #获取主角拥有的属性信息  属性：主角-异刃
        masterEleInfo = {}
        for masterName,blades in master.items():
            eleInfo = {}
            for b in blades:
                element =  blade[b]['element']
                if element not in masterEleInfo:
                     masterEleInfo[element] = []
                masterEleInfo[element].append(masterName+'-'+b)
    #    print  json.dumps(masterEleInfo, encoding='UTF-8', ensure_ascii=False)
        #看看每个组合是否满足combo
        final = {}
        for cb in combo:
            resCombo =  self.findCombo(cb,masterEleInfo)
            if resCombo is not None:
                cbjoin =   '-'.join(cb) 
                final[cbjoin] = []
                for r in resCombo:
                    final[cbjoin].append(r)
        return final
