from django.conf.urls import url
from appschoolsubjects import views

app_name = "appschoolsubjects"

urlpatterns = [
    url(r'^add/schoolsubject$', views.addSchoolSubject, name="addSchoolSubject"),
    url(r'^add/(?P<subject_id>[0-9]+)/(?P<student_id>[0-9]+)$', views.addGradeToStudent, name="addGradeToStudent"),
]
