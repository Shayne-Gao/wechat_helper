from django.conf.urls import url 

from . import wsmud
from . import mail
urlpatterns = [ 
    url(r'^wsmud_record',wsmud.post_record),
    url(r'^mail',mail.sendMail),
]
