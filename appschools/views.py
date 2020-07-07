from django.shortcuts import render, HttpResponseRedirect, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from appprofiles.models import Profile, ActivationKeys
from appschools.models import SchoolClass, School

from appschools.forms import SchoolForm, SchoolClassForm, ChangeSemesterForm,ChangeShiftForm
from appprofiles.forms import UserForm, PrincipalForm, AllTeachersOfSchool

from helper.accounts import getUsername

@login_required(login_url='/profiles/login/')
def schoolClasses(request):
    current_user = Profile.objects.get(user = request.user)
    if not current_user.is_principal:
        return render(request, "permission_denied.html", {"msg": "You dont have permissions to access the site settings. Only principals can do that.","current_user": current_user,})

    classes_of_my_school = SchoolClass.objects.filter(school = current_user.school)

    if request.method == "POST":
        school_class_form = SchoolClassForm(request.POST)
        if school_class_form.is_valid():
            school_class = school_class_form.save(commit = False)
            school_class.school = current_user.school
            school_class.save()

            return HttpResponseRedirect(reverse('appschools:schoolClasses', args=()))
    school_class_form = SchoolClassForm()
    teachers = Profile.objects.filter(school = current_user.school, is_teacher=True).exclude(school_class = None)

    teachers_dict = {}
    for teacher in teachers:
        if teacher.school_class in classes_of_my_school:
            teachers_dict[classes_of_my_school.get(id = teacher.school_class.id)] = teacher

    return render(request, "appschools/school_classes.html", {
        "current_user": current_user,
        "school_class_form": school_class_form,
        "classes_of_my_school":classes_of_my_school,
        "teachers_dict": teachers_dict,
    })

@login_required(login_url='/profiles/login/')
def schoolSettings(request):
    current_user = Profile.objects.get(user = request.user)
    if Profile.objects.filter(school = current_user.school, is_principal = True).count() > 0:
        current_principal = Profile.objects.get(school = current_user.school, is_principal = True)
    else:
        current_principal = "doesnt exist"
    #if not current_user.is_siteadmin:  return render(request, "permission_denied.html", {"msg": "You dont have permissions to access the site settings. Only site admins can do that.","current_user": current_user,})
    shift = ""
    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        if current_user.is_teacher:
            shift = ChangeShiftForm(request.POST, instance = SchoolClass.objects.get(id = current_user.school_class.id))
        principal_form = PrincipalForm(request.POST, request.FILES)
        all_teachers = AllTeachersOfSchool(request.POST, user = request.user)
        change_semester_form = ChangeSemesterForm(request.POST, instance = School.objects.get(id = current_user.school.id))
        if user_form.is_valid() and principal_form.is_valid():

            if Profile.objects.filter(school = current_user.school, is_principal = True).count() > 0:
                """
                if statement checks if there is a principal. If there already a user with
                is_principal = True, it sets the is_principal to False
                """
                current_principal = Profile.objects.get(school = current_user.school, is_principal = True)
                current_principal.is_principal = False
                current_principal.save()

            user = user_form.save(commit = False)
            user.username = getUsername(request.POST.get("first_name"),request.POST.get("last_name"))
            user.set_password("asd")
            user.save()

            principal = principal_form.save(commit = False)
            principal.user = user
            principal.school = current_user.school
            principal.is_principal = True
            principal.profile_pic = principal_form.cleaned_data['profile_pic']
            principal.save()

            return HttpResponseRedirect(reverse('appschools:schoolSettings', args=()))
        elif all_teachers.is_valid():
            if Profile.objects.filter(school = current_user.school, is_principal = True).count() > 0:
                """
                if statement checks if there is a principal. If there already a user with
                is_principal = True, it sets the is_principal to False
                """
                current_principal = Profile.objects.get(school = current_user.school, is_principal = True)
                current_principal.is_principal = False
                current_principal.save()

            teacher = request.POST.get("teachers")
            Profile.objects.filter(id = teacher).update(is_principal=True)
            return HttpResponseRedirect(reverse('appschools:schoolSettings', args=()))

        elif change_semester_form.is_valid():
            change_semester_form.save()
            return HttpResponseRedirect(reverse('appschools:schoolSettings', args=()))
        elif shift.is_valid():
            print(shift)
            shift.save()
            return HttpResponseRedirect(reverse('appschools:schoolSettings', args=()))
        else:
            return HttpResponse("Form not valid")

    if current_user.is_teacher:
        shift = ChangeShiftForm(initial={'shift': current_user.school_class.shift})
    principal_form = PrincipalForm()
    user_form = UserForm()
    allTeachers = AllTeachersOfSchool(user = request.user)
    change_semester_form = ChangeSemesterForm(initial={'semester': current_user.school.semester})
    return render(request, "appschools/school_settings.html", {
        "current_user": current_user,
        "principal_form":principal_form,
        "user_form":user_form,
        "current_principal": current_principal,
        "change_semester_form":change_semester_form,
        "allTeachers": allTeachers,
        "shift": shift,
    })

def schoolActivation(request, sec_key=""):
    if sec_key and not request.user.is_authenticated():
        request.session['sec_key'] = sec_key
        return redirect("/profiles/login/")
    if request.user.is_authenticated() and request.session.get('sec_key'):
        current_user = Profile.objects.get(user = request.user)
        if ActivationKeys.objects.get(user = current_user, sec_key = request.session.get('sec_key')):
            school = School.objects.get(id = current_user.school.id)
            school.is_active = True
            school.save()
            del request.session['sec_key']
            return redirect("appprofiles:home")
    return HttpResponse("Something is wrong")
