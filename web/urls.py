from django.conf.urls import url 

from . import views
from . import xb2tools
from . import wf
from . import price
from . import accountbook
from . import ro
from . import wsmud
urlpatterns = [ 
    url(r'^wf/list', wf.priceList),
    url(r'^wf/price', wf.price),
    url(r'^wf/build', wf.build),
    url(r'^wf', views.wf_tool),
    url(r'^sbn_tool',views.sbn_tool),
    url(r'^sbn_result',views.sbn_result),
    url(r'^price_searcher',price.price_searcher),
    url(r'^act',accountbook.detail),
    url(r'^ro',ro.index),
    url(r'^change_type',accountbook.modifyRecordType),
    url(r'^xb2_combo$',xb2tools.xb2_combo),
    url(r'^xb2_combo_result',xb2tools.combo_result),
    url(r'^wsmud/status',wsmud.status),
    url(r'^$', views.index, name='index'),
]
