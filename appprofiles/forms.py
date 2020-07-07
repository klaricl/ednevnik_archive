from django import forms
from django.contrib.auth.models import User
from appprofiles.models import Profile
from appschools.models import SchoolClass

THEMES = (
    ("dark", "dark"),
    ("light", "light"),
)

class UserForm(forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput())
    #username = forms.CharField(label = False, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.CharField(label = False, widget=forms.TextInput(attrs={'placeholder': 'Email'}), required=False)
    #password = forms.CharField(label = False, widget=forms.TextInput(attrs={'placeholder': 'Password'}))
    first_name = forms.CharField(label = False, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(label = False, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email', )


class SAUserForm(forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput())
    #username = forms.CharField(label = False, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.CharField(label = False, widget=forms.TextInput(attrs={'placeholder': 'Email'}), required=False)
    password = forms.CharField(label = False, widget=forms.TextInput(attrs={'placeholder': 'Password'}))
    first_name = forms.CharField(label = False, widget=forms.TextInput(attrs={'placeholder': 'First name'}))
    last_name = forms.CharField(label = False, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    class Meta():
        model = User
        fields = ('first_name', 'last_name', 'email', 'password',)

class SiteAdminForm(forms.ModelForm):
    password = forms.CharField(label = False, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password=forms.CharField(label = False, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}))
    class Meta():
        model = Profile
        fields = ()

    def clean(self):
        cleaned_data = super(SiteAdminForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

class PrincipalForm(forms.ModelForm):
    is_teacher = forms.BooleanField(label="Je li predavac", required = False)
    class Meta():
        model = Profile
        fields = ('is_teacher','profile_pic',)

class AllTeachersOfSchool(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AllTeachersOfSchool,self).__init__(*args, **kwargs)
        userProfile = Profile.objects.get(user = user)
        self.fields['teachers'].queryset = Profile.objects.filter(school = userProfile.school, is_teacher = True)

    teachers = forms.ModelChoiceField(queryset = Profile.objects.all(), label = False)

class TeacherForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ('school_class','profile_pic',)

class StudentForm(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ('profile_pic',)

class TeacherToClassForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(TeacherToClassForm,self).__init__(*args, **kwargs)
        userProfile = Profile.objects.get(user = user)
        self.fields['teachers'].queryset = Profile.objects.filter(school = userProfile.school, is_teacher = True).filter(school_class = None)
        self.fields['classes'].queryset = SchoolClass.objects.filter(has_teacher = False).filter(school = userProfile.school, has_teacher = False)

    teachers = forms.ModelChoiceField(queryset = Profile.objects.all(), label = False)
    classes = forms.ModelChoiceField(queryset = SchoolClass.objects.all(), label = False)

class ChangeProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ChangeProfileForm, self).__init__(*args, **kwargs)
        userProfile = Profile.objects.get(user = user)
        self.fields['theme'].initial = userProfile.theme
        #theme = userProfile.theme
        #print(theme)

    theme = forms.ChoiceField(choices=THEMES)
    class Meta:
        model = Profile
        fields = ('theme',)
