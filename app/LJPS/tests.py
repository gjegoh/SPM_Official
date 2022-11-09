from http import client
from pydoc import cli
from urllib import request, response
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from .models import Skill
from DB_init.enums import Skill_Course_Category, Status
from .views import *
import json

# Create your tests here.
class TestSkills(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.get(username='admin')
        self.client = Client()
        self.delete_skill = reverse('delete_skill')
        self.update_skill = reverse('update_skill')
        self.create_skill = reverse('create_skill')
        Skill.objects.create(Skill_Category=Skill_Course_Category.CORE, Skill_Name="Interpersonal Skills", Skill_Status=Status.ACTIVE)
    
    def test_skill_creation(self):
        interpersonal_skill = Skill.objects.get(Skill_Name="Interpersonal Skills")
        self.assertEqual(interpersonal_skill.Skill_Name, 'Interpersonal Skills')
        self.assertEqual(interpersonal_skill.Skill_Category, Skill_Course_Category.CORE)
        self.assertEqual(interpersonal_skill.Skill_Status, Status.ACTIVE)

    def test_plan_skill_view(self):
        request = self.factory.get('LJPS/plan_skill.html')
        request.user = self.user
        response = plan_skill(request)
        self.assertEqual(response.status_code, 200)
    
    def test_manage_skill_view(self):
        request = self.factory.get('LJPS/manage_skill.html')
        request.user = self.user
        response = manage_skill(request)
        self.assertEqual(response.status_code, 200)

    def test_edit_skill_view(self):
        interpersonal_skill = Skill.objects.get(Skill_Name="Interpersonal Skills")
        request = self.factory.get('LJPS/edit_skill.html')
        request.user = self.user
        response = edit_skill(request, interpersonal_skill.Skill_ID )
        self.assertEqual(response.status_code, 200)

    def test_create_skill_post_success(self):
        response = self.client.post(self.create_skill, {
            'skill_id': 50,
            'skill_category': Skill_Course_Category.CORE,
            'skill_name': "New Marketing Development", 
            'skill_status': Status.ACTIVE
        })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['status'], 'success')
        self.assertEquals(response.context['message'], 'You have successfully created a skill!')

    def test_create_skill_post_failure_duplicate_name(self):
        response = self.client.post(self.create_skill, {
            'skill_id': 51,
            'skill_category': Skill_Course_Category.CORE,
            'skill_name': "Interpersonal Skills", 
            'skill_status': Status.ACTIVE
        })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['status'], 'failed')
        self.assertEquals(response.context['message'], 'A skill with your specified name already exists!')

    def test_update_skill_post_success(self):
        response = self.client.post(self.update_skill, {
            'skill_id': 1,
            'skill_category': Skill_Course_Category.CORE,
            'skill_name': "New Interpersonal Skills", 
            'skill_status': Status.RETIRED
        })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['status'], 'success')
        self.assertEquals(response.context['message'], 'You have successfully updated a skill!') 

    def test_update_skill_post_failure_no_changes(self):
        response = self.client.post(self.update_skill, {
            'skill_id': 1,
            'skill_category': Skill_Course_Category.SALES,
            'skill_name': "Affiliate Marketing", 
            'skill_status': Status.ACTIVE
        })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['status'], 'failed')
        self.assertEquals(response.context['message'], 'No changes to the skill was made!!')   

    def test_update_skill_post_failure_duplicate_name(self):
        response = self.client.post(self.update_skill, {
            'skill_id': 1,
            'skill_category': Skill_Course_Category.CORE,
            'skill_name': "Interpersonal Skills", 
            'skill_status': Status.RETIRED
        })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['status'], 'failed')
        self.assertEquals(response.context['message'], 'A skill with your specified name already exists!')

    def test_delete_skill(self):
        response = self.client.post(
            self.delete_skill,
            content_type='application/json', 
            data=json.dumps({'skill_id': 1})
        )
        self.assertEquals(response.status_code, 200)

    

    





   

    

  
