from django.shortcuts import render, redirect

from appprofiles.models import Profile
from .models import SchoolScheduler,LessonPlan,PresenceOfStudent
from appschoolsubjects.models import SchoolSubject

from appschoolscheduler.forms import ScheduleSubjectForm
# Create your views here.

def schedule(request):
    current_user = Profile.objects.get(user = request.user)
    if current_user.school_class == None:
        return render(request, "permission_denied.html", {"msg": "You dont have permissions to view the scheduler. Only class teachers can view the schedules to their classes.","current_user": current_user,})
    schedule = SchoolScheduler.objects.filter(school_class = current_user.school_class)

    form = ScheduleSubjectForm(user = current_user)

    return render(request, "appschoolscheduler/schedule.html",
        {
            "current_user": current_user,
            "form": form,
            "schedule": schedule,
        })

def setSchedule(request, order, day):
    current_user = Profile.objects.get(user = request.user)
    print("order: %s" % order)
    print("day: %s" % day)
    print("razred: %s" % current_user.school_class)
    print("smjena: %s" % current_user.school_class.shift)
    print("predmet: %s" % request.POST.get("school_subject", ""))

    if SchoolScheduler.objects.filter(day = day, order = order, school_class = current_user.school_class, active = True):
        current_active = SchoolScheduler.objects.get(day = day, order = order, school_class = current_user.school_class, active = True)
        current_active.active = False
        current_active.save()

    query = SchoolScheduler(
        school_class = current_user.school_class,
        subject = SchoolSubject.objects.get(id = request.POST.get("school_subject", "")),
        day = day,
        order = order,
        shift = current_user.school_class.shift,
        teacher = SchoolSubject.objects.get(id = request.POST.get("school_subject", "")).teacher
    )
    query.save()

    return redirect("/schoolscheduler/schedule")

def planLesson(request, order, day, scheduled_subject):
    current_user = Profile.objects.get(user = request.user)
    s_subject = SchoolScheduler.objects.get(id = scheduled_subject)
    print("####################################################")
    print(type(s_subject.subject))
    query = LessonPlan(
        scheduled_subject = SchoolScheduler.objects.get(id = scheduled_subject),
        lesson = request.POST.get("lesson", ""),
        subject = s_subject.subject,
    )
    query.save()
    return redirect("/profiles/home")

def presenceOfStudent(request, order, day, subject):
    current_user = Profile.objects.get(user = request.user)
    print(SchoolScheduler.objects.get(id = subject))
    print(request.POST.get("justified", ""))
    print(request.POST.get("notes", ""))
    print(Profile.objects.get(id = request.POST.get("students", "")))

    query = PresenceOfStudent(
        scheduled_subject = SchoolScheduler.objects.get(id = subject),
        justified = bool(request.POST.get("justified", "")),
        notes = request.POST.get("notes", ""),
        student = Profile.objects.get(id = request.POST.get("students", "")),
        semester = current_user.school.semester,
    )
    query.save()

    return redirect("/profiles/home")
