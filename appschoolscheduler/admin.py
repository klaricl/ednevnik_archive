from django.contrib import admin
from .models import SchoolScheduler,LessonPlan,PresenceOfStudent

# Register your models here.

class SchoolSchedulerAdmin(admin.ModelAdmin):
    list_display = ('id', 'active', 'shift', 'order', 'day', 'teacher')

admin.site.register(SchoolScheduler,SchoolSchedulerAdmin)
admin.site.register(LessonPlan)
admin.site.register(PresenceOfStudent)
