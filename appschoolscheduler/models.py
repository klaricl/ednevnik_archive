from django.db import models
import datetime
from appschoolsubjects.models import SchoolSubject
from appschools.models import SchoolClass
from appprofiles.models import Profile


# Create your models here.

class SchoolScheduler(models.Model):
    school_class = models.ForeignKey(SchoolClass)
    subject = models.ForeignKey(SchoolSubject)
    teacher = models.ForeignKey(Profile, null = True)
    day = models.IntegerField()
    order = models.IntegerField()
    shift = models.IntegerField()
    active = models.BooleanField(default = True)

    def __str__(self):
        return "{}".format(self.subject)

class LessonPlan(models.Model):
    scheduled_subject = models.ForeignKey(SchoolScheduler)
    lesson = models.TextField(null = True)
    date = models.DateField(default=datetime.date.today)
    subject = models.ForeignKey(SchoolSubject, null = True)
    def __str__(self):
        return "{}".format(self.scheduled_subject)

class PresenceOfStudent(models.Model):
    date = models.DateField(default=datetime.date.today)
    scheduled_subject = models.ForeignKey(SchoolScheduler)
    justified = models.BooleanField(default = True)
    notes = models.TextField(blank = True)
    student = models.ForeignKey(Profile)
    semester = models.IntegerField()
    def __str__(self):
        return "{}".format(self.student)
