#!/usr/bin/python
# -*- coding:utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import urllib
import MySQLdb
import types
import urllib2
import time
from db import AccountBookDB
from category import Category 
import datetime
from statistic import Statistic
from analysis import Analysis

from collections import defaultdict

class AccountRecord(object):

    def deleteLastRecord(self,uid,valid=AccountBookDB().REC_VALID_FALSE):
        return AccountBookDB().deleteLatestRecord(uid,valid)

    def classifyLastRecord(self,uid,typeName):
        cateId =  AccountBookDB().getCategoryIdByNameAndOtherName(typeName)
        if cateId == None:
            return 1,'Wrong Type Name'
        updateRes = AccountBookDB().updateLastRecordCate(uid,cateId);
        return updateRes

    def classifyRecordType(self,uid,rid,typeName):
        cateId =  AccountBookDB().getCategoryIdByNameAndOtherName(typeName)
        if cateId == None:
            return 1,'Wrong Type Name'
        updateRes = AccountBookDB().updateRecordCate(uid,rid,cateId);
        return updateRes

    def getLastValidRecord(self,uid):
        res = AccountBookDB().getLastValidRecord(uid);
        return res

#print AccountRecord().classifyLastRecord(1,'夫妻');
#print AccountRecord().getLastValidRecord(1);
