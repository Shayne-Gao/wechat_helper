from django.conf.urls import url 

from . import views

urlpatterns = [ 
    url(r'^/list', views.priceList),
    url(r'^/price', views.price),
    url(r'^/build', views.build),
    url(r'^/sbn_tool',views.sbn_tool),
    url(r'^/sbn_result',views.sbn_result),
    url(r'^$', views.index, name='index'),
]
