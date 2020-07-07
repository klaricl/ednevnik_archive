from django.db import models

import datetime
# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    county = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    language = models.CharField(max_length = 2, default="EN")
    semester = models.IntegerField(default = 1)
    first_shift_begin = models.TimeField(default=datetime.time(7, 30))
    second_shift_begin = models.TimeField(default=datetime.time(13, 30))

    def __str__(self):
        return self.name

class SchoolClass(models.Model):
    class_number = models.CharField(max_length = 5)
    class_direction = models.CharField(max_length = 50)
    school = models.ForeignKey(School, null=True, blank=True, on_delete=models.CASCADE)
    has_teacher = models.BooleanField(default = False)
    shift = models.IntegerField(default = 1)

    def __str__(self):
        return "%s - %s" % (self.class_number, self.class_direction)
