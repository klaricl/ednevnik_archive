from django.contrib import admin
from appschoolsubjects.models import SchoolSubject, Grades
# Register your models here.

class SchoolSubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'teacher', 'school_class')

class GradesAdmin(admin.ModelAdmin):
    list_display = ('student', 'school_subject', 'grade', 'semester')

admin.site.register(SchoolSubject, SchoolSubjectAdmin)

admin.site.register(Grades, GradesAdmin)
