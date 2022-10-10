def initial_web_app_group(sender, **kwargs):
    from django.contrib.auth.models import User
    from LJPS.models import Job_Role, Skill, Course, Role, Staff
    from .enums import System_Role, Skill_Course_Category, Course_Status, Course_Type
        
    # create mock django users, staff and roles
    if not Staff.objects.exists():
        print("###   Creating mock django users, staff and assigning roles  ###")
        Staff.objects.create(
            User=User.objects.create_superuser('admin', '', 'admin'),
            Staff_FName='HR',
            Staff_LName='Admin',
            Dept='Human Resource',
            Email='hradmin@gmail.com',
            Role=Role.objects.create(Role_Name=System_Role.ADMIN)
        )
        user_role = Role.objects.create(Role_Name=System_Role.USER)
        Staff.objects.create(
            User=User.objects.create_user('learner1', '', 'learner1'),
            Staff_FName='Learner',
            Staff_LName='One',
            Dept='Finance',
            Email='learnerone@gmail.com',
            Role=user_role
        )
        Staff.objects.create(
            User=User.objects.create_user('learner2', '', 'learner2'),
            Staff_FName='Learner',
            Staff_LName='Two',
            Dept='Operations',
            Email='learnertwo@gmail.com',
            Role=user_role
        )
        Staff.objects.create(
            User=User.objects.create_user('manager', '', 'manager'),
            Staff_FName='Manager',
            Staff_LName='Boss',
            Dept='Operations',
            Email='managerboss@gmail.com',
            Role=Role.objects.create(Role_Name=System_Role.MANAGER)
        )
    
    # create mock job roles
    if not Job_Role.objects.exists():
        print('###   Creating mock job roles   ###')
        marketing_associate = Job_Role.objects.create(
            Job_Role_Name='Marketing Associate',
            Job_Role_Desc="Supports the implementation of marketing plans"
        )
        project_financing_executive = Job_Role.objects.create(
            Job_Role_Name='Project Financing Executive',
            Job_Role_Desc="Gathers data and analyses it to support financing activities"
        )
        # project_development_engineer = Job_Role.objects.create(
        #     Job_Role_Name='Project Development Engineer',
        #     Job_Role_Desc="Drives project development activities"
        # )
        # talent_management_manager = Job_Role.objects.create(
        #     Job_Role_Name='Talent Management Manager',
        #     Job_Role_Desc="Implements programmes to groom talent in the organization"
        # )

    # create mock skills and assign skills to job roles
    if not Skill.objects.exists():
        print('###   Creating and assigning mock skills to job roles   ###')
        # Marketing Associate
        affiliate_marketing = Skill.objects.create(
            Skill_Name="Affiliate Marketing", 
            Skill_Category=Skill_Course_Category.SALES
        )
        content_management = Skill.objects.create(
            Skill_Name="Content Management", 
            Skill_Category=Skill_Course_Category.SALES 
        )
        communication = Skill.objects.create(
            Skill_Name="Communication", 
            Skill_Category=Skill_Course_Category.CORE
        )
        teamwork = Skill.objects.create(
            Skill_Name="Teamwork", 
            Skill_Category=Skill_Course_Category.CORE
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
            Skill_Category=Skill_Course_Category.FINANCE
        )
        data_and_statistical_analytics = Skill.objects.create(
            Skill_Name="Data and Statistical Analytics", 
            Skill_Category=Skill_Course_Category.FINANCE
        )
        digital_literacy = Skill.objects.create(
            Skill_Name="Digital Literacy", 
            Skill_Category=Skill_Course_Category.CORE
        )
        sense_making = Skill.objects.create(
            Skill_Name="Sense Making", 
            Skill_Category=Skill_Course_Category.CORE
        )
        project_financing_executive.Job_Role_Required_Skill.add(
            cost_management,
            data_and_statistical_analytics,
            digital_literacy,
            sense_making
        )
        # Project Development Engineer
        # business_performance_management = Skill.objects.create(
        #     Skill_Name="Business Performance Management", 
        #     Skill_Category=Skill_Course_Category.TECHNICAL 
        # )
        # organisational_risk_management = Skill.objects.create(
        #     Skill_Name="Organisational Risk Management", 
        #     Skill_Category=Skill_Course_Category.TECHNICAL
        # )
        # decision_making = Skill.objects.create(
        #     Skill_Name="Decision Making", 
        #     Skill_Category=Skill_Course_Category.GENERIC
        # )
        # problem_solving = Skill.objects.create(
        #     Skill_Name="Problem Solving", 
        #     Skill_Category=Skill_Course_Category.GENERIC 
        # )
        # project_development_engineer.Job_Role_Required_Skill.add(
        #     business_performance_management,
        #     organisational_risk_management,
        #     decision_making,
        #     problem_solving
        # )
        # Talent Management Manager
        # employee_mobility_management= Skill.objects.create(
        #     Skill_Name="Employee Mobility Management", 
        #     Skill_Category=Skill_Course_Category.TECHNICAL
        # )
        # talent_management= Skill.objects.create(
        #     Skill_Name="Talent Management", 
        #     Skill_Category=Skill_Course_Category.TECHNICAL
        # )
        # developing_people= Skill.objects.create(
        #     Skill_Name="Developing People", 
        #     Skill_Category=Skill_Course_Category.GENERIC
        # )
        # interpersonal_skills = Skill.objects.create(
        #     Skill_Name="Interpersonal Skills", 
        #     Skill_Category=Skill_Course_Category.GENERIC 
        # )
        # talent_management_manager.Job_Role_Required_Skill.add(
        #     employee_mobility_management,
        #     talent_management,
        #     developing_people,
        #     interpersonal_skills
        # )

    # create mock courses and assign skills to courses 
    if not Course.objects.exists():
        print('###   Creating mock courses and assigning skills to courses   ###')
        # sales courses
        marketing_101 = Course.objects.create(
            Course_ID='S-123',
            Course_Name='Marketing 101',
            Course_Desc='Teaches you everything about marketing',
            Course_Status=Course_Status.ACTIVE,
            Course_Type=Course_Type.INTERNAL,
            Course_Category=Skill_Course_Category.SALES
        )
        marketing_101.Course_Fulfilled_Skill.add(
            affiliate_marketing,
            content_management
        )
        intro_to_affiliate_marketing = Course.objects.create(
            Course_ID='S-321',
            Course_Name='Intro to Affiliate Marketing',
            Course_Desc='Teaches you the basics of affiliate marketing',
            Course_Status=Course_Status.ACTIVE,
            Course_Type=Course_Type.EXTERNAL,
            Course_Category=Skill_Course_Category.SALES
        )
        intro_to_affiliate_marketing.Course_Fulfilled_Skill.add(
            affiliate_marketing
        )
        intro_to_content_management = Course.objects.create(
            Course_ID='S-412',
            Course_Name='Intro to Content Management',
            Course_Desc='Teaches you the basics of content management',
            Course_Status=Course_Status.ACTIVE,
            Course_Type=Course_Type.INTERNAL,
            Course_Category=Skill_Course_Category.SALES
        )
        intro_to_content_management.Course_Fulfilled_Skill.add(
            content_management
        )
        # finance courses
        finance_101 = Course.objects.create(
            Course_ID='F-567',
            Course_Name='Finance 101',
            Course_Desc='Teaches you everything about finance',
            Course_Status=Course_Status.ACTIVE,
            Course_Type=Course_Type.EXTERNAL,
            Course_Category=Skill_Course_Category.FINANCE
        )
        finance_101.Course_Fulfilled_Skill.add(
            cost_management,
            data_and_statistical_analytics
        )
        intro_to_cost_management = Course.objects.create(
            Course_ID='F-786',
            Course_Name='Intro to Cost Management',
            Course_Desc='Teaches you the basics of cost management',
            Course_Status=Course_Status.ACTIVE,
            Course_Type=Course_Type.INTERNAL,
            Course_Category=Skill_Course_Category.FINANCE
        )
        intro_to_cost_management.Course_Fulfilled_Skill.add(
            cost_management
        )
        intro_to_data_and_statistical_analytics = Course.objects.create(
            Course_ID='F-854',
            Course_Name='Intro to Data and Statistical Analytics',
            Course_Desc='Teaches you the basics of data and statistical analytics',
            Course_Status=Course_Status.ACTIVE,
            Course_Type=Course_Type.INTERNAL,
            Course_Category=Skill_Course_Category.FINANCE
        )
        intro_to_data_and_statistical_analytics.Course_Fulfilled_Skill.add(
            data_and_statistical_analytics
        )
        # core courses
        collaboration_101 = Course.objects.create(
            Course_ID='C-705',
            Course_Name='Collaboration 101',
            Course_Desc='Teaches you everything about collaboration',
            Course_Status=Course_Status.ACTIVE,
            Course_Type=Course_Type.INTERNAL,
            Course_Category=Skill_Course_Category.CORE
        )
        collaboration_101.Course_Fulfilled_Skill.add(
            teamwork,
            communication
        )
        digital_world_101 = Course.objects.create(
            Course_ID='C-531',
            Course_Name='Digital World 101',
            Course_Desc='Teaches you everything about the digital world',
            Course_Status=Course_Status.ACTIVE,
            Course_Type=Course_Type.EXTERNAL,
            Course_Category=Skill_Course_Category.CORE
        )
        digital_world_101.Course_Fulfilled_Skill.add(
            digital_literacy,
            sense_making
        )
        # retired courses
        intro_to_communication = Course.objects.create(
            Course_ID='C-945',
            Course_Name='Intro to Communication',
            Course_Desc='Teaches you everything about how to communicate',
            Course_Status=Course_Status.RETIRED,
            Course_Type=Course_Type.EXTERNAL,
            Course_Category=Skill_Course_Category.CORE
        )
        intro_to_communication.Course_Fulfilled_Skill.add(
            communication
        )

