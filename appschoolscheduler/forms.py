from django.forms import ModelForm
from django import forms

from appschoolsubjects.models import SchoolSubject
from .models import LessonPlan,PresenceOfStudent

class ScheduleSubjectForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(ScheduleSubjectForm,self).__init__(*args, **kwargs)
        self.fields['school_subject'].queryset = SchoolSubject.objects.filter(school_class = user.school_class_id)

    school_subject = forms.ModelChoiceField(label = False, queryset = SchoolSubject.objects.all())

    class Meta:
        model = SchoolSubject
        fields = ('school_subject',)

class LessonPlanForm(ModelForm):

    class Meta:
        model = LessonPlan
        fields = ('lesson',)

class PresenceOfStudentForm(ModelForm):

    class Meta:
        model = (PresenceOfStudent)
        fields = ('notes', 'justified')
