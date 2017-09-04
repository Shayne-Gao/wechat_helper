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

tr = WmTranslator()
wdb = WarframeDB()
items = wdb.getBuildItemlikeName('')
for it in items:
    zh = tr.en2zh(it['name_en'])
    sql = """UPDATE build_item set name_zh='%s' where id=%s"""%(zh,it['id'])
    print sql
    print wdb.queryBySql(sql)
