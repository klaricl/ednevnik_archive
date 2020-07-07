from appprofiles.models import Profile
from django.contrib.auth.models import User
import random
import string

def getUsername(fname, lname):

    username = fname.lower() + "." + lname.lower()
    i = 0
    while True:
        if i == 0:
            if User.objects.filter(username = fname.lower() + "." + lname.lower()):
                i = i + 1
            else:
                return fname.lower() + "." + lname.lower()
        else:
            if User.objects.filter(username = fname.lower() + "." + lname.lower() + str(i)):
                i = i + 1
            else:
                return fname.lower() + "." + lname.lower() + str(i)

def genSecKey(size=24, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
