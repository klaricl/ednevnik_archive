from django.forms import ModelForm
from django import forms
from appprofiles.models import Profile
from appschoolsubjects.models import SchoolSubject,Grades

class AddSchoolSubjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AddSchoolSubjectForm,self).__init__(*args, **kwargs)

        self.fields['teacher'].queryset = Profile.objects.filter(school = user.school_id).filter(is_teacher = True)

    title = forms.CharField(max_length = 50, label = False, widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    teacher = forms.ModelChoiceField(label = False, queryset = Profile.objects.all())

    class Meta:
        model = SchoolSubject
        fields = ('title', 'teacher')

class AddGradeToStudent(ModelForm):
    grade = forms.ChoiceField(choices=[(x, x) for x in range(1, 6)])
    class Meta:
        model = (Grades)
        fields = ('grade', 'is_final', 'description',)
