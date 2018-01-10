from django.conf.urls import url 

from . import views
from . import xb2tools
urlpatterns = [ 
    url(r'^wf/list', views.priceList),
    url(r'^wf/price', views.price),
    url(r'^wf/build', views.build),
    url(r'^sbn_tool',views.sbn_tool),
    url(r'^sbn_result',views.sbn_result),
    url(r'^xb2_combo$',xb2tools.xb2_combo),
    url(r'^xb2_combo_result',xb2tools.combo_result),
    url(r'^$', views.index, name='index'),
]
