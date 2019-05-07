from django.conf.urls import url 

from . import wsmud
urlpatterns = [ 
    url(r'^wsmud_record',wsmud.post_record),
]
