from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from appschoolsubjects.models import SchoolSubject
from appprofiles.models import Profile

from appschoolsubjects.forms import AddSchoolSubjectForm, AddGradeToStudent
from appprofiles.forms import TeacherToClassForm

from appoverviews.views import subjectToTeach

@login_required(login_url='/profiles/login/')
def addSchoolSubject(request):
    current_user = Profile.objects.get(user = request.user)
    schoolSubjects = SchoolSubject.objects.filter(school_class = current_user.school_class)
    if current_user.school_class == None:
        return render(request, "permission_denied.html", {"msg": "You dont have permissions to add subjects. Only class teachers can add subjects to their classes.","current_user": current_user,})
    if not current_user.is_teacher:
        return render(request, "permission_denied.html", {"msg": "You dont have permissions to this site. Only class teachershace.","current_user": current_user,})
    if request.method == "POST":
        add_school_subject_form = AddSchoolSubjectForm(data = request.POST, user = current_user)
        if add_school_subject_form.is_valid():

            form = add_school_subject_form.save(commit = False)

            #form.title = add_school_subject_form.cleaned_data['title']
            #form.teacher = add_school_subject_form.cleaned_data['teacher']
            form.school_class = current_user.school_class

            form.save()
        else:
            print("The form is not valid (appschoolsubjects.addSchoolSubject)")

    add_school_subject_form = AddSchoolSubjectForm(user = current_user)
    return render(request, "appschoolsubjects/add_school_subject.html", {
        "current_user": current_user,
        "addSchoolSubjectForm": add_school_subject_form,
        "schoolSubjects": schoolSubjects,
    })

@login_required(login_url='/profiles/login/')
def addGradeToStudent(request, student_id, subject_id):
    current_user = Profile.objects.get(user = request.user)
    if not current_user.is_teacher:
        return render(request, "permission_denied.html", {"msg": "You dont have permissions to this site. Only class teachershace.","current_user": current_user,})
    my_subjects = SchoolSubject.objects.filter(teacher = current_user)
    student = Profile.objects.get(id = student_id)
    subject = SchoolSubject.objects.get(id = subject_id)

    if request.method == "POST":
        add_grade_to_student_form = AddGradeToStudent(request.POST)
        if add_grade_to_student_form.is_valid():
            form = add_grade_to_student_form.save(commit = False)

            form.student = student
            form.school_subject = subject
            form.semester = current_user.school.semester

            form.save()

            return redirect("/overviews/subject/%s" % subject_id)
