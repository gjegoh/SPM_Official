from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.models import User
from LJPS.models import Job_Role, Skill, Course, Role, Staff, Registration, Learning_Journey
from DB_init.enums import System_Role, Course_Status, Registration_Status, Completion_Status
from django.db.models import Count, Q
import json
from collections import Counter

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
            
# endpoint to render page for staff to plan their learning journey
def plan_learning_journey(request, id):
    if request.method == 'GET':
        staff = Staff.objects.get(User=request.user)
        if staff.Role.Role_Name == System_Role.USER:
            chosen_job_role = Job_Role.objects.get(Job_Role_ID=id)
            required_skill_obj = chosen_job_role.Job_Role_Required_Skill.all()
            mapped_skill_course_dict= {}
            for skill_obj in required_skill_obj:
                mapped_skill_course_dict[skill_obj] = Course.objects.filter(
                    Course_Fulfilled_Skill=skill_obj,
                    Course_Status=Course_Status.ACTIVE
                )
            return render(
                request,
                'LJPS/plan_learning_journey.html',
                context={
                    'chosen_job_role': chosen_job_role,
                    'mapped_skill_course_dict': mapped_skill_course_dict
                }
            )
        else:
            return render(
                request,
                'LJPS/plan_learning_journey.html',
            )

# endpoint to handle creation of learning journeys for staff
def create_learning_journey(request):
    if request.method == 'POST':
        course_lst = list(set(request.POST.getlist('learningJourney')))
        role= Job_Role.objects.get(Job_Role_ID=request.POST.get('job_role'))
        staff = Staff.objects.get(User=request.user)
        chosen_course_objs = []
        for course_id in course_lst:
            course = Course.objects.get(Course_ID=course_id)
            chosen_course_objs.append(course)
        duplicate_check = Learning_Journey.objects.filter(
            Staff=staff,
            Job_Role=role
        ).annotate(
            num_courses=Count('Learning_Journey_Course'),
            num_courses_match=Count(
                'Learning_Journey_Course', 
                filter=Q(Learning_Journey_Course__in=chosen_course_objs)
            )
        ).filter(
            num_courses=len(chosen_course_objs),
            num_courses_match=len(chosen_course_objs)
        )
        if duplicate_check.exists():
            message = "A learning journey with your selected courses and job role already exists!"
            status = 'failed'
        else:
            learning_journey = Learning_Journey.objects.create(
                Staff=staff,
                Job_Role=role
            )
            
            for course in chosen_course_objs:
                Registration.objects.get_or_create(
                    Course=course,
                    Staff=staff,
                    defaults={
                        'Reg_Status': Registration_Status.REGISTERED,
                        'Completion_Status': Completion_Status.ONGOING
                    }
                )
                learning_journey.Learning_Journey_Course.add(course)
            message = "You have successfully created a learning journey!"
            status = 'success'
        return render(
            request,
            'LJPS/create_learning_journey.html',
            context={
                'message': message,
                'status': status
            }
        )

# endpoint to render page for staff to view/edit their created learning journeys
def view_learning_journey(request):
    if request.method == 'GET':
        staff = Staff.objects.get(User=request.user)
        learning_journey_lst = Learning_Journey.objects.filter(Staff=staff)
        mapped_learning_journey = {}
        for learning_journey in learning_journey_lst:
            mapped_course_skill = {}
            course_lst = learning_journey.Learning_Journey_Course.all()
            skill_lst = learning_journey.Job_Role.Job_Role_Required_Skill.all()
            for course in course_lst:
                course_status = Registration.objects.get(
                    Course=course,
                    Staff=staff
                ).Completion_Status
                mapped_course_skill[course.Course_Name] = {
                    'course_status': course_status,
                    'fulfilled_skills': course.Course_Fulfilled_Skill.all()
                }
            mapped_skill_course = {}
            for skill in skill_lst:
                related_course_lst = []
                for course_name in mapped_course_skill:
                    if skill in mapped_course_skill[course_name]['fulfilled_skills']:
                        related_course_lst.append({
                            'course_name': course_name,
                            'course_status': mapped_course_skill[course_name]['course_status']
                        })
                mapped_skill_course[skill.Skill_Name] = related_course_lst
            mapped_learning_journey[learning_journey.Learning_Journey_ID] = {
                'job_role': learning_journey.Job_Role.Job_Role_Name,
                'mapped_skill_course': mapped_skill_course
            } 
        return render(
            request,
            'LJPS/view_learning_journey.html',
            context={
                'mapped_learning_journey': mapped_learning_journey
            }
        )

# endpoint to render page for staff to edit learning journey
def edit_learning_journey(request, id):
    if request.method == 'GET':
        staff = Staff.objects.get(User=request.user)
        if staff.Role.Role_Name == System_Role.USER:
            chosen_learning_journey = Learning_Journey.objects.get(Learning_Journey_ID=id)
            chosen_job_role = chosen_learning_journey.Job_Role
            required_skill_obj = chosen_job_role.Job_Role_Required_Skill.all()
            chosen_course_objs = chosen_learning_journey.Learning_Journey_Course.all()
            mapped_skill_course_dict= {}
            for skill_obj in required_skill_obj:
                related_course_dict = {}
                related_course_lst = Course.objects.filter(
                    Course_Fulfilled_Skill=skill_obj,
                    Course_Status=Course_Status.ACTIVE
                )
                for course in related_course_lst:
                    if course in chosen_course_objs:
                        related_course_dict[course] = True
                    else:
                        related_course_dict[course] = False
                mapped_skill_course_dict[skill_obj] = related_course_dict
            return render(
                request,
                'LJPS/edit_learning_journey.html',
                context={
                    'chosen_learning_journey': id,
                    'chosen_job_role': chosen_job_role,
                    'mapped_skill_course_dict': mapped_skill_course_dict
                }
            )
        else:
            return render(
                request,
                'LJPS/edit_learning_journey.html',
            )

# endpoint to handle update of learning journeys for staff
def update_learning_journey(request):
    if request.method == 'POST':
        new_course_lst = list(set(request.POST.getlist('learningJourney')))
        learning_journey_id = int(request.POST.get('learning_journey_id'))
        learning_journey = Learning_Journey.objects.get(Learning_Journey_ID=learning_journey_id)
        old_course_lst = learning_journey.Learning_Journey_Course.all()
        staff = Staff.objects.get(User=request.user)
        new_course_objs = []
        for course_id in new_course_lst:
            course = Course.objects.get(Course_ID=course_id)
            new_course_objs.append(course)
        if Counter(new_course_objs) == Counter(old_course_lst):
            message = "No changes to your learning journey was made!"
            status = 'failed'
        else:
            duplicate_check = Learning_Journey.objects.filter(
                Staff=staff,
                Job_Role=learning_journey.Job_Role.Job_Role_ID
            ).annotate(
                num_courses=Count('Learning_Journey_Course'),
                num_courses_match=Count(
                    'Learning_Journey_Course', 
                    filter=Q(Learning_Journey_Course__in=new_course_objs)
                )
            ).filter(
                num_courses=len(new_course_objs),
                num_courses_match=len(new_course_objs)
            )
            if duplicate_check.exists():
                message = "A learning journey with your selected courses and job role already exists!"
                status = 'failed'
            else:
                for course in new_course_objs:
                    if course not in old_course_lst:
                        Registration.objects.get_or_create(
                            Course=course,
                            Staff=staff,
                            defaults={
                                'Reg_Status': Registration_Status.REGISTERED,
                                'Completion_Status': Completion_Status.ONGOING
                            }
                        )
                        learning_journey.Learning_Journey_Course.add(course)
                for course in old_course_lst:
                    if course not in new_course_objs:
                        Registration.objects.get(
                            Course=course,
                            Staff=staff,
                        ).delete()
                        learning_journey.Learning_Journey_Course.remove(course)
                message = "You have successfully updated your learning journey!"
                status = 'success'
        return render(
            request,
            'LJPS/update_learning_journey.html',
            context={
                'message': message,
                'status': status
            }
        )

# endpoint to delete learning journey for staff
def delete_learning_journey(request):
    if request.method == 'POST':
        request_body = json.loads(request.body)
        learning_journey_id = request_body['learning_journey_id']
        Learning_Journey.objects.get(Learning_Journey_ID=learning_journey_id).delete()
        return HttpResponse(200)

# endpoint to render page for admin to manage job roles
def manage_job_roles(request):
    if request.method == 'GET':
        staff = Staff.objects.get(User=request.user)
        if staff.Role.Role_Name == System_Role.ADMIN:
            job_role_obj = Job_Role.objects.order_by('Job_Role_Name')
            return render(
                request,
                'LJPS/manage_job_roles.html',
                context={
                    'job_role_obj': job_role_obj,
                }
            )
        else:
            return render(
                request,
                'LJPS/manage_job_roles.html',
            )

# endpoint to render page for admin to edit job role
def edit_job_role(request, id):
    if request.method == 'GET':
        staff = Staff.objects.get(User=request.user)
        if staff.Role.Role_Name == System_Role.ADMIN:
            chosen_job_role = Job_Role.objects.get(Job_Role_ID=id)
            all_skills = Skill.objects.filter(Skill_Status=Status.ACTIVE)
            assigned_skills = chosen_job_role.Job_Role_Required_Skill.all()
            return render(
                request,
                'LJPS/edit_job_roles.html',
                context={
                    'chosen_job_role': chosen_job_role,
                    'all_skills': all_skills,
                    'assigned_skills': assigned_skills
                }
            )
        else:
            return render(
                request,
                'LJPS/edit_job_roles.html',
            )
            
# endpoint to handle update of job roles for admin
def update_job_role(request):
    if request.method == 'POST':
        message = "You have successfully updated your learning journey!"
        status = 'success'
        changed_name = False
        new_skill_lst = list(set(request.POST.getlist('assigned_skills')))
        job_role_id = int(request.POST.get('job_role_id'))
        new_job_role_name = request.POST.get('job_role_name')
        job_role = Job_Role.objects.get(Job_Role_ID=job_role_id)
        if new_job_role_name.lower() != job_role.Job_Role_Name.lower():
            if len(Job_Role.objects.filter(Job_Role_Name__iexact=new_job_role_name)) > 0:
                message = "A job role with your updated job role name already exists!"
                status = 'failed'
            else:
                Job_Role.objects.filter(Job_Role_ID=job_role_id).update(Job_Role_Name=new_job_role_name.title())
                changed_name = True
        if status == 'success':
            changed_desc = False
            new_job_role_desc = request.POST.get('job_role_desc')
            if new_job_role_desc.lower() != job_role.Job_Role_Desc.lower():
                Job_Role.objects.filter(Job_Role_ID=job_role_id).update(Job_Role_Desc=new_job_role_desc)
                changed_desc = True
            changed_status = False
            new_job_role_status = request.POST.get('job_role_status')
            if new_job_role_status != job_role.Job_Role_Status:
                Job_Role.objects.filter(Job_Role_ID=job_role_id).update(Job_Role_Status=new_job_role_status)
                changed_status = True
            old_skill_lst = job_role.Job_Role_Required_Skill.all()
            staff = Staff.objects.get(User=request.user)
            new_skill_obj = []
            for skill_id in new_skill_lst:
                skill = Skill.objects.get(Skill_ID=skill_id)
                new_skill_obj.append(skill)
            skill_unchanged = Counter(new_skill_obj) == Counter(old_skill_lst)
            if skill_unchanged and changed_name == False and changed_desc == False and changed_status == False:
                message = "No changes to the job role was made!"
                status = 'failed'
            elif skill_unchanged == False:
                duplicate_check = Job_Role.objects.annotate(
                    num_courses=Count('Job_Role_Required_Skill'),
                    num_courses_match=Count(
                        'Job_Role_Required_Skill', 
                        filter=Q(Job_Role_Required_Skill__in=new_skill_obj)
                    )
                ).filter(
                    num_courses=len(new_skill_obj),
                    num_courses_match=len(new_skill_obj)
                )
                if duplicate_check.exists():
                    message = "A job role with your assigned skills already exists!"
                    status = 'failed'
                else:
                    for skill in new_skill_obj:
                        if skill not in old_skill_lst:
                            job_role.Job_Role_Required_Skill.add(skill)
                    for skill in old_skill_lst:
                        if skill not in new_skill_obj:
                            job_role.Job_Role_Required_Skill.remove(skill)
        return render(
            request,
            'LJPS/update_job_role.html',
            context={
                'message': message,
                'status': status
            }
        )

# endpoint to render page for admin to plan job role
def plan_job_role(request):
    if request.method == 'GET':
        staff = Staff.objects.get(User=request.user)
        if staff.Role.Role_Name == System_Role.ADMIN:
            all_skills = Skill.objects.filter(Skill_Status=Status.ACTIVE)
            return render(
                request,
                'LJPS/plan_job_role.html',
                context={
                    'all_skills': all_skills
                }
            )
        else:
            return render(
                request,
                'LJPS/plan_job_role.html',
            )

# endpoint to handle creation of job roles for admin
def create_job_role(request):
    if request.method == 'POST':
        message = "You have successfully created a job role!"
        status = 'success'
        skill_lst = list(set(request.POST.getlist('assigned_skills')))
        job_role_name = request.POST.get('job_role_name')
        job_role_desc = request.POST.get('job_role_desc')
        job_role_status = request.POST.get('job_role_status')
        if len(Job_Role.objects.filter(Job_Role_Name__iexact=job_role_name)) > 0:
            message = "A job role with your specified name already exists!"
            status = 'failed'
        else:
            skill_obj = []
            for skill_id in skill_lst:
                skill = Skill.objects.get(Skill_ID=skill_id)
                skill_obj.append(skill)
            duplicate_check = Job_Role.objects.annotate(
                num_courses=Count('Job_Role_Required_Skill'),
                num_courses_match=Count(
                    'Job_Role_Required_Skill', 
                    filter=Q(Job_Role_Required_Skill__in=skill_obj)
                )
            ).filter(
                num_courses=len(skill_obj),
                num_courses_match=len(skill_obj)
            )
            if duplicate_check.exists():
                message = "A job role with your assigned skills already exists!"
                status = 'failed'
            else:
                new_job_role = Job_Role.objects.create(
                    Job_Role_Name=job_role_name.title(),
                    Job_Role_Desc=job_role_desc,
                    Job_Role_Status=job_role_status
                )
                for skill in skill_obj:
                    new_job_role.Job_Role_Required_Skill.add(skill)
        return render(
            request,
            'LJPS/create_job_role.html',
            context={
                'message': message,
                'status': status
            }
        )

# endpoint to toggle job role status for admin
def toggle_job_role_status(request):
    if request.method == 'POST':
        request_body = json.loads(request.body)
        job_role_id = request_body['job_role_id']
        job_role = Job_Role.objects.get(Job_Role_ID=job_role_id)
        if job_role.Job_Role_Status == Status.ACTIVE:
            Job_Role.objects.filter(Job_Role_ID=job_role_id).update(Job_Role_Status=Status.RETIRED)
        else:
            Job_Role.objects.filter(Job_Role_ID=job_role_id).update(Job_Role_Status=Status.ACTIVE)
        return HttpResponse(200)
    
# endpoint to delete job role for admin
def delete_job_role(request):
    if request.method == 'POST':
        request_body = json.loads(request.body)
        job_role_id = request_body['job_role_id']
        Job_Role.objects.get(Job_Role_ID=job_role_id).delete()
        return HttpResponse(200)