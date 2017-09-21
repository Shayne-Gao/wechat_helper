# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

#!/usr/bin/python
# -*- coding:utf-8 -*- 
import sys
reload(sys)
sys.path.append("..")
sys.setdefaultencoding('utf-8')


# Create your tests here.
request = "12.4哈哈哈123"
request = request.decode('utf-8') # to unicode
print request
for k,c in enumerate(request):
    if c >= '\u4e00' and c<= '\u9fa5':
        cost=request[0:k]
        content=request[k:]
        print k,cost,content
print None
