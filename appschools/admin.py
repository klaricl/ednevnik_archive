from django.contrib import admin
from appschools.models import School, SchoolClass

# Register your models here.
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_number', 'class_direction', 'school', 'has_teacher')


admin.site.register(School)
admin.site.register(SchoolClass, SchoolClassAdmin)
