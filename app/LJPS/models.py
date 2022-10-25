from django.db import models
from django.contrib.auth.models import User

class Staff(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Staff_ID = models.BigAutoField(primary_key=True)
    Staff_FName = models.CharField(max_length=50)
    Staff_LName = models.CharField(max_length=50)
    Dept = models.CharField(max_length=50)
    Email = models.EmailField(max_length=50)
    Role = models.ForeignKey('Role', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.Staff_FName + self.Staff_LName
    
class Role(models.Model):
    Role_ID = models.BigAutoField(primary_key=True)
    Role_Name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.Role_Name

class Registration(models.Model):
    Reg_ID = models.BigAutoField(primary_key=True)
    Course = models.ForeignKey('Course', on_delete=models.CASCADE) 
    Staff = models.ForeignKey('Staff', on_delete=models.CASCADE) 
    Reg_Status = models.CharField(max_length=20)
    Completion_Status = models.CharField(max_length=20)

class Skill(models.Model):
    Skill_ID = models.BigAutoField(primary_key=True)
    Skill_Name = models.CharField(max_length=50)
    Skill_Category = models.CharField(max_length=50)
    Skill_Status = models.CharField(max_length=15, null=True, blank=True)
    
    def __str__(self):
        return self.Skill_Name

class Course(models.Model):
    Course_ID = models.CharField(max_length=20, primary_key=True)
    Course_Name = models.CharField(max_length=50)
    Course_Desc = models.CharField(max_length=255)
    Course_Status = models.CharField(max_length=15, null=True, blank=True)
    Course_Type = models.CharField(max_length=10)
    Course_Category = models.CharField(max_length=50)
    Course_Fulfilled_Skill = models.ManyToManyField(Skill)
    
    def __str__(self):
        return self.Course_Name
    
class Learning_Journey(models.Model):
    Learning_Journey_ID = models.BigAutoField(primary_key=True)
    Staff = models.ForeignKey('Staff', on_delete=models.CASCADE) 
    Job_Role = models.ForeignKey('Job_Role', on_delete=models.CASCADE) 
    Learning_Journey_Course = models.ManyToManyField(Course)

class Job_Role(models.Model):
    Job_Role_ID = models.BigAutoField(primary_key=True)
    Job_Role_Name = models.CharField(max_length=50)
    Job_Role_Desc = models.TextField()
    Job_Role_Required_Skill = models.ManyToManyField(Skill)
    Job_Role_Status = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.Job_Role_Name
