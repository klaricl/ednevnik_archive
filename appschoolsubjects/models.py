from django.db import models
from appprofiles.models import Profile
from appschools.models import SchoolClass

# Create your models here.

class SchoolSubject(models.Model):
    title = models.CharField(max_length = 50)
    teacher = models.ForeignKey(Profile)
    school_class = models.ForeignKey(SchoolClass, null = True, blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.title)


class Grades(models.Model):
    student = models.ForeignKey(Profile)
    school_subject = models.ForeignKey(SchoolSubject)
    grade = models.IntegerField()
    description = models.TextField(null = True)
    semester = models.IntegerField(null = True)
    is_final = models.BooleanField(default = False)
    semester = models.IntegerField(default = 1)
    is_final = models.BooleanField(default = False)

    def __unicode__(self):
        return "{},{}".format(self.school_subject, self.grade)
