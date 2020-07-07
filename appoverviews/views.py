from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from appprofiles.models import Profile
from appschools.models import SchoolClass
from appschoolsubjects.models import SchoolSubject, Grades
from appschoolscheduler.models import PresenceOfStudent

from appschoolsubjects.forms import AddGradeToStudent

@login_required(login_url='/profiles/login/')
def subjectToTeach(request, subject_id):
    """ Subject To teach
    This form shows a subject of a teacher and all the students in the class.
    In this form the teacher can add grades and final grades to a student.

    forms: addGradeToStudentForm

    models: Profile, SchoolSubject, Grades

    return: permission_denied.html, appoverviews/class.html
    """
    current_user = Profile.objects.get(user = request.user)
    if current_user.is_teacher == False:
        return render(request, "permission_denied.html", {"msg": "You dont have permissions to access this form. Only class teachers can access this form.","current_user": current_user,})

    subject = SchoolSubject.objects.get(id = subject_id)
    school_class = SchoolClass.objects.get(id = subject.school_class.id)

    grades_first = Grades.objects.filter(school_subject = subject, semester = 1, is_final = False)
    grades_second = Grades.objects.filter(school_subject = subject, semester = 2, is_final = False)

    grades_first_final = Grades.objects.filter(school_subject = subject, semester = 1, is_final = True)
    grades_second_final = Grades.objects.filter(school_subject = subject, semester = 2, is_final = True)

    grades_dict_first = {}
    grades_dict_second = {}
    grades_dict_first_final = {}
    grades_dict_second_final = {}

    for grade in grades_first_final:
        grades_dict_first_final[grade.student] = ""
        if grade.grade:
            grades_dict_first_final[grade.student] = grade.grade

    for grade in grades_second_final:
        grades_dict_second_final[grade.student] = ""
        if grade.grade:
            grades_dict_second_final[grade.student] = grade.grade

    for grade in grades_first:
        if grade.student not in grades_dict_first:
            grades_dict_first[grade.student] = []
        grades_dict_first[grade.student].append(grade.grade)

    for grade in grades_second:
        if grade.student not in grades_dict_second:
            grades_dict_second[grade.student] = []
        grades_dict_second[grade.student].append(grade.grade)

    students_of_class = Profile.objects.filter(is_student = True, school_class = school_class)
    addGradeToStudentForm = AddGradeToStudent()
    return render(request, "appoverviews/class.html", {
        "current_user": current_user,
        "subject": subject,
        "students": students_of_class,
        "school_class": school_class,
        "grades_dict_first": grades_dict_first,
        "grades_dict_second": grades_dict_second,
        "grades_dict_first_final": grades_dict_first_final,
        "grades_dict_second_final": grades_dict_second_final,
        "addGradeToStudentForm":addGradeToStudentForm,
    })

@login_required(login_url='/profiles/login/')
def student(request, student_id):
    current_user = Profile.objects.get(user = request.user)

    student = Profile.objects.get(id = student_id)

    absences_justified = PresenceOfStudent.objects.filter(student = student, justified = True)
    absences_unjustified = PresenceOfStudent.objects.filter(student = student, justified = False)
    
    subjects = SchoolSubject.objects.filter(school_class = student.school_class)
    grades_first = Grades.objects.filter(student = student, semester = 1, is_final = False)
    grades_second = Grades.objects.filter(student = student, semester = 2, is_final = False)

    grades_first_final = Grades.objects.filter(student = student, semester = 1, is_final = True)
    grades_second_final = Grades.objects.filter(student = student, semester = 2, is_final = True)

    grades_dict_first = {}
    grades_dict_second = {}
    grades_dict_first_final = {}
    grades_dict_second_final = {}

    for grade in grades_first_final:
        grades_dict_first_final[grade.school_subject] = ""
        if grade.grade:
            grades_dict_first_final[grade.school_subject] = grade.grade

    for grade in grades_second_final:
        grades_dict_second_final[grade.school_subject] = ""
        if grade.grade:
            grades_dict_second_final[grade.school_subject] = grade.grade
            print(grades_dict_second_final[grade.school_subject])

    for grade in grades_first:
        if grade.school_subject not in grades_dict_first:
            grades_dict_first[grade.school_subject] = []
        grades_dict_first[grade.school_subject].append(grade.grade)

    for grade in grades_second:
        if grade.school_subject not in grades_dict_second:
            grades_dict_second[grade.school_subject] = []
        grades_dict_second[grade.school_subject].append(grade.grade)

    return render(request, "appoverviews/student.html", {
        "current_user":current_user,
        "student": student,
        "subjects": subjects,
        "grades_dict_first": grades_dict_first,
        "grades_dict_second": grades_dict_second,
        "grades_dict_first_final":grades_dict_first_final,
        "grades_dict_second_final":grades_dict_second_final,
        "absences_justified":absences_justified,
        "absences_unjustified":absences_unjustified,
    })

@login_required(login_url='/profiles/login/')
def teacher(request, teacher_id):
    """
    show the information of the teacher
    """
    teacher = Profile.objects.get(id = teacher_id)
    subjects = SchoolSubject.objects.filter(teacher=teacher)
    return render(request, "appoverviews/teacher.html", {
        "teacher": teacher,
        "subjects":subjects,
    })

@login_required(login_url='/profiles/login/')
def principal(request, principal_id):
    """
    shows the information of the principal
    """
    principal = Profile.objects.get(id = principal_id)
    pass
