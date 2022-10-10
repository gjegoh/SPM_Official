from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from LJPS.models import Job_Role, Skill, Course, Role, Staff, Registration, Learning_Journey
from DB_init.enums import System_Role, Course_Status, Registration_Status, Completion_Status
import json

# endpoint to render index page for all users
def index(request):
    if request.method == 'GET':
        return render(
            request,
            'LJPS/index.html'
        )

# renders registration page for all users
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

# endpoint to render view job roles page for staff
def view_job_roles(request):
    if request.method == 'GET':
        staff = Staff.objects.get(User=request.user)
        if staff.Role.Role_Name == System_Role.USER:
            job_role_obj = Job_Role.objects.all()
            return render(
                request,
                'LJPS/view_job_roles.html',
                context={
                    'job_role_obj': job_role_obj,
                }
            )
        else:
            return render(
                request,
                'LJPS/view_job_roles.html',
            )