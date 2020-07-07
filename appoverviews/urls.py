from django.conf.urls import url
from appoverviews import views

app_name = "appoverviews"

urlpatterns = [
    url(r'^subject/(?P<subject_id>[0-9]+)$', views.subjectToTeach, name="subjectToTeach"),
    url(r'^student/(?P<student_id>[0-9]+)$', views.student, name="student"),
    url(r'^teacher/(?P<teacher_id>[0-9]+)$', views.teacher, name="teacher"),
    url(r'^principal/(?P<principal_id>[0-9]+)$', views.principal, name="principal"),
]
