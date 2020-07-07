from django.forms import ModelForm
from django import forms
from appschools.models import School, SchoolClass

class SchoolForm(ModelForm):
    name = forms.CharField(label = False, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    country = forms.CharField(label = False, widget=forms.TextInput(attrs={'placeholder': 'Country'}))
    location = forms.CharField(label = False, widget=forms.TextInput(attrs={'placeholder': 'location'}))
    county = forms.CharField(label = False, widget=forms.TextInput(attrs={'placeholder': 'county'}))
    address = forms.CharField(label = False, widget=forms.TextInput(attrs={'placeholder': 'address'}))
    class Meta:
        model = School
        exclude = ['is_active', 'language', 'semester','first_shift_begin', 'second_shift_begin']

    def clean(self):
        super().clean()

class SchoolClassForm(ModelForm):
    class_number = forms.CharField(label = False, widget=forms.TextInput(attrs={'placeholder': 'Class number'}))
    class_direction = forms.CharField(label = False, widget=forms.TextInput(attrs={'placeholder': 'Direction'}))
    class Meta:
        model = SchoolClass
        exclude = ['school', 'has_teacher']

    def clean(self):
        super().clean()

class ChangeSemesterForm(ModelForm):
    semester = forms.ChoiceField(choices=[(x, x) for x in range(1, 3)])
    class Meta:
        model = School
        fields = ('semester',)

class ChangeShiftForm(ModelForm):
    shift =  forms.ChoiceField(choices=[(x, x) for x in range(1, 3)])

    class Meta:
        model = SchoolClass
        fields = ('shift',)
