from django.conf.urls import url
from appschools import views

app_name = "appschools"

urlpatterns = [
    url(r'^schoolclasses/$', views.schoolClasses, name="schoolClasses"),
    url(r'^schoolsettings/', views.schoolSettings, name="schoolSettings"),
    url(r'^schoolactivation/(?P<sec_key>.*)/$', views.schoolActivation, name="schoolActivation"),
    url(r'^schoolactivation/', views.schoolActivation, name="schoolActivation"),
]
