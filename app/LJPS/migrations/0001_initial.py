# Generated by Django 4.1.1 on 2022-10-10 07:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('Course_ID', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('Course_Name', models.CharField(max_length=50)),
                ('Course_Desc', models.CharField(max_length=255)),
                ('Course_Status', models.CharField(max_length=15)),
                ('Course_Type', models.CharField(max_length=10)),
                ('Course_Category', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Job_Role',
            fields=[
                ('Job_Role_ID', models.BigAutoField(primary_key=True, serialize=False)),
                ('Job_Role_Name', models.CharField(max_length=50)),
                ('Job_Role_Desc', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('Role_ID', models.BigAutoField(primary_key=True, serialize=False)),
                ('Role_Name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('Skill_ID', models.BigAutoField(primary_key=True, serialize=False)),
                ('Skill_Name', models.CharField(max_length=50)),
                ('Skill_Category', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('Staff_ID', models.BigAutoField(primary_key=True, serialize=False)),
                ('Staff_FName', models.CharField(max_length=50)),
                ('Staff_LName', models.CharField(max_length=50)),
                ('Dept', models.CharField(max_length=50)),
                ('Email', models.EmailField(max_length=50)),
                ('Role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='LJPS.role')),
                ('User', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('Reg_ID', models.BigAutoField(primary_key=True, serialize=False)),
                ('Reg_Status', models.CharField(max_length=20)),
                ('Completion_Status', models.CharField(max_length=20)),
                ('Course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LJPS.course')),
                ('Staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LJPS.staff')),
            ],
        ),
        migrations.CreateModel(
            name='Learning_Journey',
            fields=[
                ('Learning_Journey_ID', models.BigAutoField(primary_key=True, serialize=False)),
                ('Job_Role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LJPS.job_role')),
                ('Learning_Journey_Course', models.ManyToManyField(to='LJPS.course')),
                ('Staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LJPS.staff')),
            ],
        ),
        migrations.AddField(
            model_name='job_role',
            name='Job_Role_Required_Skill',
            field=models.ManyToManyField(to='LJPS.skill'),
        ),
        migrations.AddField(
            model_name='course',
            name='Course_Fulfilled_Skill',
            field=models.ManyToManyField(to='LJPS.skill'),
        ),
    ]
