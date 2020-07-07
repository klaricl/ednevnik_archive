from django import template
from django.http import HttpResponse

from helper.scheduler import get_time_of_teaching

from appschools.models import School, SchoolClass
from appprofiles.models import Profile
from appschoolsubjects.models import SchoolSubject
from appschoolscheduler.models import SchoolScheduler,LessonPlan

import datetime
register = template.Library()

@register.assignment_tag
def get_class_time(user, order):
    school = School.objects.get(id = user.school.id)
    schoolClass = SchoolClass.objects.get(id = user.school_class.id)
    if schoolClass.shift == 1:
        return get_time_of_teaching(int(order), school.first_shift_begin)
    elif schoolClass.shift == 2:
        return get_time_of_teaching(int(order), school.second_shift_begin)
    else:
        return HttpResponse("Shift is invalid")

@register.assignment_tag
def get_class_time_shift(user, order, shift):
    school = School.objects.get(id = user.school.id)
    schoolClass = SchoolClass.objects.get(id = user.school_class.id)
    if shift == 1:
        return get_time_of_teaching(int(order), school.first_shift_begin)
    elif shift == 2:
        return get_time_of_teaching(int(order), school.second_shift_begin)
    else:
        return HttpResponse("Shift is invalid")

@register.assignment_tag
def get_subject(user, order, day):
    if(SchoolScheduler.objects.filter(school_class = user.school_class, day = day, order = order, active = True)):
        return SchoolScheduler.objects.get(school_class = user.school_class, day = day, order = order, active = True)
    return ""

@register.assignment_tag
def get_subject_teacher_first_shift(user, order, day):
    if(SchoolScheduler.objects.filter(teacher = user, day = day, order = order, shift = 1, active = True)):
        return SchoolScheduler.objects.get(teacher = user, day = day, order = order, active = True, shift = 1)
    return ""

@register.assignment_tag
def get_subject_teacher_second_shift(user, order, day):
    if(SchoolScheduler.objects.filter(teacher = user, day = day, order = order, active = True, shift = 2)):
        return SchoolScheduler.objects.get(teacher = user, day = day, order = order, active = True, shift = 2)
    return ""

@register.assignment_tag
def get_scheduled_subject(user, order, day):
    if(SchoolScheduler.objects.filter(teacher = user, day = day, order = order, active = True)):
        return (SchoolScheduler.objects.get(teacher = user, day = day, order = order, active = True)).id

@register.assignment_tag
def get_students_id(user, order, day):
    if(SchoolScheduler.objects.filter(teacher = user, day = day, order = order, active = True)):
        subject = SchoolScheduler.objects.get(teacher = user, day = day, order = order, active = True)
        students = Profile.objects.filter(school_class = subject.school_class, is_student = True)
        for student in students:
            yield student.id

@register.assignment_tag
def get_student(student):
    return Profile.objects.get(id = student)

@register.assignment_tag
def get_lesson_history(subject):

    if LessonPlan.objects.filter(subject = subject.subject):
        return LessonPlan.objects.filter(subject = subject.subject)
