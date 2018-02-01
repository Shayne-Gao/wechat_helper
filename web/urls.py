from django.conf.urls import url 

from . import views
from . import xb2tools
from . import wf
from . import price
urlpatterns = [ 
    url(r'^wf/list', wf.priceList),
    url(r'^wf/price', wf.price),
    url(r'^wf/build', wf.build),
    url(r'^sbn_tool',views.sbn_tool),
    url(r'^sbn_result',views.sbn_result),
    url(r'^price_searcher',price.price_searcher),
    url(r'^xb2_combo$',xb2tools.xb2_combo),
    url(r'^xb2_combo_result',xb2tools.combo_result),
    url(r'^$', views.index, name='index'),
]
