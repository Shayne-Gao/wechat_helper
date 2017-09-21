from django.conf.urls import url 

from . import views

urlpatterns = [ 
    #url(r'^', web.index),
    url(r'^$', views.index, name='index'),
]
