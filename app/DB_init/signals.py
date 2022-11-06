def initial_web_app_group(sender, **kwargs):
    from django.contrib.auth.models import User
    from LJPS.models import Job_Role, Skill, Course, Role, Staff, Registration
    from django.conf import settings
    from .enums import System_Role, Skill_Course_Category, Status, Course_Type, Department
    import csv
    import os

    # import roles csv
    if not Role.objects.exists():
        print("###   Importing role.csv  ###")
        role_csv = open("static/role.csv")
        roles = csv.reader(role_csv)
        next(roles, None)
        role_dict = {}
        for role in roles:
            role_dict[role[0]] = Role.objects.create(Role_ID=int(role[0]), Role_Name=role[1])
    
    # import staff csv
    if not Staff.objects.exists():
        print("###   Importing staff.csv  ###")
        # create mock django user accounts
        admin = User.objects.create_superuser('admin', '', 'admin')
        learner1 = User.objects.create_user('learner1', '', 'learner1')
        staff_csv = open("static/staff.csv")
        staffs = csv.reader(staff_csv)
        next(staffs, None)
        admin_count = 0
        learner_count = 0
        for staff in staffs:
            if staff[5] == '1' and admin_count < 1:
                Staff.objects.create(
                    User=admin,
                    Staff_ID=int(staff[0]),
                    Staff_FName=staff[1],
                    Staff_LName=staff[2],
                    Dept=staff[3],
                    Email=staff[4],
                    Role=role_dict[staff[5]]
                )
                admin_count += 1
            elif staff[5] == '2' and learner_count < 1:
                Staff.objects.create(
                    User=learner1,
                    Staff_ID=int(staff[0]),
                    Staff_FName=staff[1],
                    Staff_LName=staff[2],
                    Dept=staff[3],
                    Email=staff[4],
                    Role=role_dict[staff[5]]
                )
                learner_count += 1
            else:
                Staff.objects.create(
                    Staff_ID=int(staff[0]),
                    Staff_FName=staff[1],
                    Staff_LName=staff[2],
                    Dept=staff[3],
                    Email=staff[4],
                    Role=role_dict[staff[5]]
                )
    
    # create mock job roles
    if not Job_Role.objects.exists():
        print('###   Creating mock job roles   ###')
        marketing_associate = Job_Role.objects.create(
            Job_Role_Name='Marketing Associate',
            Job_Role_Desc="Supports the implementation of marketing plans",
            Job_Role_Status=Status.ACTIVE
        )
        project_financing_executive = Job_Role.objects.create(
            Job_Role_Name='Project Financing Executive',
            Job_Role_Desc="Gathers data and analyses it to support financing activities",
            Job_Role_Status=Status.ACTIVE
        )
        project_development_engineer = Job_Role.objects.create(
            Job_Role_Name='Project Development Engineer',
            Job_Role_Desc="Drives project development activities",
            Job_Role_Status=Status.RETIRED
        )

    # create mock skills and assign skills to job roles
    if not Skill.objects.exists():
        print('###   Creating and assigning mock skills to job roles   ###')
        # Marketing Associate
        affiliate_marketing = Skill.objects.create(
            Skill_Name="Affiliate Marketing", 
            Skill_Category=Skill_Course_Category.SALES,
            Skill_Status=Status.ACTIVE
        )
        content_management = Skill.objects.create(
            Skill_Name="Content Management", 
            Skill_Category=Skill_Course_Category.SALES,
            Skill_Status=Status.ACTIVE
        )
        communication = Skill.objects.create(
            Skill_Name="Communication", 
            Skill_Category=Skill_Course_Category.CORE,
            Skill_Status=Status.ACTIVE
        )
        teamwork = Skill.objects.create(
            Skill_Name="Teamwork", 
            Skill_Category=Skill_Course_Category.CORE,
            Skill_Status=Status.ACTIVE
        )
        marketing_associate.Job_Role_Required_Skill.add(
            affiliate_marketing,
            content_management,
            communication,
            teamwork
        )
        # Project Financing Executive
        cost_management = Skill.objects.create(
            Skill_Name="Cost Management", 
            Skill_Category=Skill_Course_Category.FINANCE,
            Skill_Status=Status.ACTIVE
        )
        data_and_statistical_analytics = Skill.objects.create(
            Skill_Name="Data and Statistical Analytics", 
            Skill_Category=Skill_Course_Category.FINANCE,
            Skill_Status=Status.ACTIVE
        )
        digital_literacy = Skill.objects.create(
            Skill_Name="Digital Literacy", 
            Skill_Category=Skill_Course_Category.CORE,
            Skill_Status=Status.ACTIVE
        )
        sense_making = Skill.objects.create(
            Skill_Name="Sense Making", 
            Skill_Category=Skill_Course_Category.CORE,
            Skill_Status=Status.ACTIVE
        )
        project_financing_executive.Job_Role_Required_Skill.add(
            cost_management,
            data_and_statistical_analytics,
            digital_literacy,
            sense_making
        )
        # Project Development Engineer
        business_performance_management = Skill.objects.create(
            Skill_Name="Business Performance Management", 
            Skill_Category=Skill_Course_Category.SALES,
            Skill_Status=Status.RETIRED
        )
        project_development_engineer.Job_Role_Required_Skill.add(
            communication,
            teamwork
        )

    # import course.csv
    if not Course.objects.exists():
        print('###   Importing course.csv   ###')
        course_csv = open("static/courses.csv", encoding='cp1252')
        courses = csv.reader(course_csv)
        next(courses, None)
        course_count = 0
        core_count = 0
        non_core_count = 0
        course_dict_1 = {
            0: [affiliate_marketing, content_management],
            1: [affiliate_marketing],
            2: [content_management],
            3: [cost_management, data_and_statistical_analytics],
            4: [cost_management],
            5: [data_and_statistical_analytics]
        }
        course_dict_2 = {
            0: [teamwork, communication],
            1: [digital_literacy, sense_making]
        }
        for course in courses:
            course[1] = Course.objects.create(
                Course_ID=course[0],
                Course_Name=course[1],
                Course_Desc=course[2],
                Course_Status=course[3],
                Course_Type=course[4],
                Course_Category=course[5]
            )
            if course_count < 8 and course[3] == Status.ACTIVE:
                if course[5] == Skill_Course_Category.CORE and core_count < 2:
                    for skill in course_dict_2[core_count]:
                        course[1].Course_Fulfilled_Skill.add(skill)
                    course_count += 1
                    core_count += 1
                elif course[5] != Skill_Course_Category.CORE and non_core_count < 6:
                    for skill in course_dict_1[non_core_count]:
                        course[1].Course_Fulfilled_Skill.add(skill)
                    course_count += 1
                    non_core_count += 1

    # import registration.csv
    if not Registration.objects.exists():
        print('###   Importing registration.csv   ###')
        reg_csv = open("static/registration.csv")
        regs = csv.reader(reg_csv)
        next(regs, None)
        for reg in regs:
            Registration.objects.create(
                Reg_ID=int(reg[0]),
                Course=Course.objects.get(Course_ID=reg[1]),
                Staff=Staff.objects.get(Staff_ID=int(reg[2])),
                Reg_Status=reg[3],
                Completion_Status=reg[4]
            )
