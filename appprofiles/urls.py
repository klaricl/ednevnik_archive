from django.conf.urls import url
from appprofiles import views

app_name = "appprofiles"

urlpatterns = [
    url(r'^login/$', views.userLogin, name="login"),
    url(r'^logout/$', views.userLogout, name="logout"),
    url(r'^decline/$', views.userDecline, name="decline"),
    url(r'^home/$', views.homeView, name="home"),
    url(r'^teachers/$', views.teachers, name="teachers"),
    url(r'^students/$', views.students, name="students"),
]
