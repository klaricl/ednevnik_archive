from django.conf.urls import url
from appschoolscheduler import views

app_name = "appschoolscheduler"

urlpatterns = [
    url(r'^schedule/$', views.schedule, name = "schedule"),
    url(r'^schedule/(?P<order>[0-9]+)/(?P<day>[0-9]+)$', views.setSchedule, name = "setschedule"),
    url(r'^schedule/(?P<order>[0-9]+)/(?P<day>[0-9]+)/(?P<scheduled_subject>\w+)$', views.planLesson, name = "planlesson"),
    url(r'^schedule/presence/(?P<order>[0-9]+)/(?P<day>[0-9]+)/(?P<subject>\w+)$', views.presenceOfStudent, name = "presenceofstudent"),
]
