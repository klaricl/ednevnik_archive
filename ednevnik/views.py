from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from appschools.forms import SchoolForm
from appprofiles.forms import UserForm, SiteAdminForm
from appmessages.forms import ContactMessagesForm

#from appschools.models import School
from appprofiles.models import ActivationKeys

from helper.accounts import getUsername, genSecKey


def index(request):
    """The index of the E-Dnevnik site

    This is the root site. Includes the contacting form so everyone could send a message
    to the admin.

    returns: index.html

    forms: ContactMessagesForm
    """
    msg_form = ContactMessagesForm()
    return render(request, "index.html", {"msg_form":msg_form})

def denied(request):
    """Denies the acces to a site

    This view will be called if a permission issue occurs.

    returns: permission_denied.html
    """
    return render(request, "permission_denied.html")

def registration(request):
    """Registration form for registering an Site Admin and a school

    The view takes data from the registration.html. It creates an user for authentication,
    enters the profile data in the Profile model and creates a school.
    The will not be activated at the first. The Site Admin gets an e-mail with a link.
    He has to open his mail and confirm his registration by clicking on this link.
    Afterwards the school will be activated, the Site Admin can sign in and start with
    updating his school.

    forms: UserForm, SchoolForm, SiteAdminForm

    models: ActivationKeys

    returns: registration.html, /registration, index

    """
    if request.user.is_authenticated(): return HttpResponse("you are allready logged in and also a member of a school")
    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        school_form = SchoolForm(data = request.POST)
        site_admin_form = SiteAdminForm(data = request.POST)

        if user_form.is_valid() and school_form.is_valid() and site_admin_form.is_valid():
            # Saving the user for authentication
            user = user_form.save(commit = False)
            user.username = getUsername(request.POST.get("first_name"),request.POST.get("last_name"))
            user.set_password(request.POST.get("password"))
            user.save()

            # Saving the school
            school = school_form.save()

            # Saving the profile data of the user
            site_admin = site_admin_form.save(commit=False)
            site_admin.user = user
            site_admin.school = school
            site_admin.is_siteadmin = True
            site_admin.save()

            # Generating a seckey used for confirmation in the mail
            sec_key = genSecKey()

            # Saving a new input in the ActiovationKeys model (user and seckey)
            activation_key = ActivationKeys()
            activation_key.user = site_admin
            activation_key.sec_key = sec_key
            activation_key.save()


            message = "Hello %s!" % user.first_name
            message += "Your username is %s" % user.username
            message += "Activate your school here: http://localhost:8000/schools/schoolactivation/%s/" % sec_key
            send_mail(
                'Activate your school',
                message,
                'omikron.ednevnik@1988@gmail.com',
                [user.email],
                fail_silently=False,
            )

            return redirect("index")
        return redirect("/registration")
    else:

        schoolForm = SchoolForm()
        userForm = UserForm()
        siteAdminForm = SiteAdminForm()
        return render(request, "registration.html", {'schoolForm': schoolForm,
                                                     'userForm': userForm,
                                                     'siteAdminForm': siteAdminForm,})
