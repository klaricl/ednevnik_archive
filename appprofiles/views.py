from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse

from appprofiles.models import Profile
from appschools.models import SchoolClass
from appschoolsubjects.models import SchoolSubject, Grades

from appprofiles.forms import UserForm, PrincipalForm, TeacherForm, StudentForm, TeacherToClassForm, ChangeProfileForm
from appschoolscheduler.forms import LessonPlanForm,PresenceOfStudentForm

from helper.accounts import getUsername

# Create your views here.

def userLogin(request):
    """ User login

    View for the user to login. Dont uses any forms. If not POST,
    the view return the login form. If POST, the view takes the
    username and password and try to login.
    The view has also the function to check if the user is active.
    If the user is not active, it means that the school is not active,
    and he cannot login. At first login he has to use the link sent to
    the users mail. The link has a SecKey at the end. This SecKey is used
    to check that this user made the registration. If the SecKey from the link
    and the SecKey for the user in the model are the same, the user and the
    school will be activated.

    returns: /schools/schoolactivation/, /profiles/home/, appprofiles/login.html

    """
    if request.user.is_authenticated(): return HttpResponse("Your are already logged in")
    error_msg = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            # User and School activation process
            if user.is_active:
                login(request,user)
                current_user = Profile.objects.get(user = request.user)
                print(request.session.get('sec_key'))
                if request.session.get('sec_key') and not current_user.school.is_active:
                    return redirect("/schools/schoolactivation/")
                return redirect('/profiles/home/')
        else:
            error_msg = "Wrong username or password. Please try again!"
            return render(request,"appprofiles/login.html", {"error_msg": error_msg})
    return render(request,"appprofiles/login.html", {})

@login_required(login_url='/profiles/login/')
def userLogout(request):
    """ User logout

    View for log out. Redirects to root "/"

    """
    logout(request)
    return redirect('/')

@login_required(login_url='/profiles/login/')
def userDecline(request):
    """ User decline

    Declines the user to work further because the school is not active.
    Log the user automatically out and throws a message.

    returns: 'Your school is not active!'
    """
    logout(request)
    return HttpResponse('Your school is not active!')

@login_required(login_url='/profiles/login/')
def homeView(request):
    current_user = Profile.objects.get(user = request.user)
    if not current_user.school.is_active: return redirect('/profiles/decline/')

    my_subjects = ""
    grades_first_dict = ""
    grades_second_dict = ""
    lesson_plan_form = ""
    presence_of_student = ""

    if current_user.is_principal:
        role = "principal"
        if current_user.is_teacher:
            role = "principal (teacher)"
    elif current_user.is_teacher:
        role = "teacher"

        my_subjects = SchoolSubject.objects.filter(teacher = current_user)
        lesson_plan_form = LessonPlanForm()
        presence_of_student = PresenceOfStudentForm()
        print(lesson_plan_form)
        print("WERE ARE HERE")
    elif current_user.is_student:
        role = "student"
        grades_first = Grades.objects.filter(student = current_user, semester = 1)
        grades_second = Grades.objects.filter(student = current_user, semester = 2)
        subjects = SchoolSubject.objects.filter(school_class = current_user.school_class)

        grades_first_dict = {}
        grades_second_dict = {}

        for subject in subjects:
            grades_first_dict[subject] = []
            grades_second_dict[subject] = []

        for grade in grades_first:
            grades_first_dict[grade.school_subject].append(grade.grade)

        for grade in grades_second:
            grades_second_dict[grade.school_subject].append(grade.grade)

    elif current_user.is_siteadmin: role = "site admin"

    if request.method == "POST":
            change_profile_form = ChangeProfileForm(data = request.POST, user = request.user)
            if change_profile_form.is_valid():
                print("Im in the change")

                change_profile = change_profile_form.save(commit = False)
                change_profile.theme = request.POST.get('theme', "")
                print(request.POST.get('theme', ""))
                current_user.theme = request.POST.get('theme', "")
                current_user.save()

                return HttpResponseRedirect(reverse('appprofiles:home', args=()))


    change_profile_form = ChangeProfileForm(user = request.user)
    print("###############################################")
    user_profile = {
        "current_user": current_user,
        "role": role,
        "my_subjects": my_subjects,
        'grades_first': grades_first_dict,
        'grades_second': grades_second_dict,
        "change_profile_form":change_profile_form,
        "lesson_plan_form": lesson_plan_form,
        "presence_of_student": presence_of_student,
    }
    return render(request,"appprofiles/home_view.html", user_profile)

@login_required(login_url='/profiles/login/')
def teachers(request):
    current_user = Profile.objects.get(user = request.user)
    teachers_of_my_school = Profile.objects.filter(school = current_user.school, is_teacher = True)
    if not current_user.is_siteadmin and not current_user.is_principal:
        return render(request, "permission_denied.html", {"msg": "You dont have permissions to access this form. Only class principals can access this form.","current_user": current_user,})

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        teacher_form = TeacherForm(request.POST, request.FILES)
        assing_teacher_to_class_form = TeacherToClassForm(data = request.POST, user = request.user)

        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save(commit = False)
            user.username = getUsername(request.POST.get("first_name"),request.POST.get("last_name"))
            user.set_password("asd")
            user.save()

            teacher = teacher_form.save(commit = False)
            teacher.user = user
            teacher.school = current_user.school
            teacher.is_teacher = True
            teacher.profile_pic = teacher_form.cleaned_data['profile_pic']
            teacher.save()

            return HttpResponseRedirect(reverse('appprofiles:teachers', args=()))

        elif assing_teacher_to_class_form.is_valid():
            if assing_teacher_to_class_form.is_valid():
                teacher = request.POST.get("teachers")
                schoolClass = request.POST.get("classes")
                Profile.objects.filter(id = teacher).update(school_class=schoolClass)
                SchoolClass.objects.filter(id = schoolClass).update(has_teacher = True)
        else:
            return HttpResponse("Form not valid")

    teacher_form = TeacherForm()
    user_form = UserForm()
    assing_teacher_to_class_form = TeacherToClassForm(user = request.user)

    return render(request,"appprofiles/teachers.html", {
        "current_user": current_user,
        "teacher_form": teacher_form,
        "user_form": user_form,
        "teachers_of_my_school": teachers_of_my_school,
        "assing_teacher_to_class_form":assing_teacher_to_class_form,
    })

@login_required(login_url='/profiles/login/')
def students(request):
    current_user = Profile.objects.get(user = request.user)
    students_of_my_class = Profile.objects.filter(school_class = current_user.school_class, is_student = True)
    if not current_user.is_teacher: return render(request, "permission_denied.html", {"msg": "You are not a teacher. You cant create students."})
    if current_user.school_class == None: return render(request, "permission_denied.html", {"msg": "You dont have an class assigned. You cant create students."})

    if request.method == "POST":
        user_form = UserForm(data = request.POST)
        student_form = StudentForm(request.POST, request.FILES)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save(commit = False)
            user.username = getUsername(request.POST.get("first_name"),request.POST.get("last_name"))
            user.set_password("asd")
            user.save()

            student = student_form.save(commit = False)
            student.user = user
            student.school = current_user.school
            student.school_class = current_user.school_class
            student.profile_pic = student_form.cleaned_data['profile_pic']
            student.is_student = True
            student.save()
            return HttpResponseRedirect(reverse('appprofiles:students', args=()))
        else:
            return HttpResponse("Form is not valid (appprofiles.students)")
    student_form = StudentForm()
    user_form = UserForm()
    return render(request, "appprofiles/students.html", {
        "current_user": current_user,
        "student_form": student_form,
        "user_form": user_form,
        "students_of_my_class":students_of_my_class
    })
