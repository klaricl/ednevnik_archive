from django.conf.urls import url
from appmessages import views

app_name = "appmessages"

urlpatterns = [
    url(r'^contact/$', views.contactMsgHandler, name="contact_msg_handler"),
]
