from django.contrib import admin
from .models import Staff, Course, Role, Registration, Skill, Job_Role, Learning_Journey

class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "User",
        "Staff_ID",
        "Staff_FName",
        "Staff_LName",
        "Dept",
        "Role"
    )
admin.site.register(Staff, StaffAdmin)

class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "Course_ID",
        "Course_Name",
        "Course_Status"
    )
admin.site.register(Course, CourseAdmin)

class RoleAdmin(admin.ModelAdmin):
    list_display = (
        "Role_ID",
        "Role_Name"
    )
admin.site.register(Role, RoleAdmin)

class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "Reg_ID",
        "Course",
        "Staff",
        "Reg_Status",
        "Completion_Status"
    )
admin.site.register(Registration, RegistrationAdmin)

class SkillAdmin(admin.ModelAdmin):
    list_display = (
        "Skill_ID",
        "Skill_Name",
        "Skill_Status"
    )
admin.site.register(Skill, SkillAdmin)

class Job_RoleAdmin(admin.ModelAdmin):
    list_display = (
        "Job_Role_ID",
        "Job_Role_Name",
        "Job_Role_Status"
    )
admin.site.register(Job_Role, Job_RoleAdmin)

class Learning_JourneyAdmin(admin.ModelAdmin):
    list_display = (
        "Learning_Journey_ID",
        "Staff",
        "Job_Role"
    )
admin.site.register(Learning_Journey, Learning_JourneyAdmin)
