from django.db import models
from appschools.models import School, SchoolClass
from django.contrib.auth.models import User

# Create your models here.

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'profile_images/{0}/{1}'.format(instance.user.id, filename)

class Profile(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    school = models.ForeignKey(School, null=True, blank=True,on_delete=models.CASCADE)
    school_class = models.ForeignKey(SchoolClass, null = True, blank=True,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to = user_directory_path, default = "profile_images/unknown.png")
    is_siteadmin = models.BooleanField(default = False)
    is_principal = models.BooleanField(default = False)
    is_teacher = models.BooleanField(default = False)
    is_student = models.BooleanField(default = False)
    language = models.CharField(max_length = 2, default="EN")
    theme = models.CharField(max_length = 30, default="dark")

    def __str__(self):
        return "{}".format(self.user)

class ActivationKeys(models.Model):
    user = models.ForeignKey(Profile)
    sec_key = models.CharField(max_length = 25)
    activated = models.BooleanField(default=False)
