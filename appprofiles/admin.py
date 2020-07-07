from django.contrib import admin
from appprofiles.models import Profile, ActivationKeys

# Register your models here.

#admin.site.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school', 'school_class', 'roles', 'profile_pic')
    search_fields = ('user__first_name', 'user__last_name')
    def roles(self, obj):
        roles = ""
        if obj.is_siteadmin: roles += "SA"
        if obj.is_principal: roles += "P"
        if obj.is_teacher: roles += "T"
        if obj.is_student: roles += "S"
        return roles
    roles.allow_tags = True
    roles.short_description = 'Roles'

admin.site.register(Profile, ProfileAdmin)

admin.site.register(ActivationKeys)
