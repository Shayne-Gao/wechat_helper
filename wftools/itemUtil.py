#!/usr/bin/python
# -*- coding:utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from lxml import etree
import requests
import json
import urllib
import MySQLdb
import types
import urllib2
import time
import httplib
from db import WarframeDB
from translator import WmTranslator
from BuildStatic import BuildStatic
 

class ItemUtil:
   def getItemImgByZh(self,nameZh):
        sql = """SELECT item_img from item where name_zh = '%s' limit 1 """ %(nameZh)
        res = WarframeDB().queryBySql(sql)
        if len(res) == 0:
            return 'None'
        return res[0][0]
#print ItemUtil().getItemImgByZh('弹指瞬技')

