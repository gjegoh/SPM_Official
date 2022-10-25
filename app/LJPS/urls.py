from django.urls import path
from . import views
from .views import SignUpView

urlpatterns = [
    path('', views.index, name='index'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("view_job_roles/", views.view_job_roles, name="view_job_roles"),
    path("plan_learning_journey/<int:id>/", views.plan_learning_journey, name="plan_learning_journey"),
    path("create_learning_journey/", views.create_learning_journey, name="create_learning_journey"),
    path("view_learning_journey/", views.view_learning_journey, name="view_learning_journey"),
    path("edit_learning_journey/<int:id>/", views.edit_learning_journey, name="edit_learning_journey"),
    path("update_learning_journey/", views.update_learning_journey, name="update_learning_journey"),
    path("delete_learning_journey/", views.delete_learning_journey, name="delete_learning_journey"),
    path("manage_job_roles/", views.manage_job_roles, name="manage_job_roles"),
    path("edit_job_role/<int:id>/", views.edit_job_role, name="edit_job_role"),
    path("update_job_role/", views.update_job_role, name="update_job_role"),
    path("plan_job_role/", views.plan_job_role, name="plan_job_role"),
    path("create_job_role/", views.create_job_role, name="create_job_role"),
    path("toggle_job_role_status/", views.toggle_job_role_status, name="toggle_job_role_status"),
    path("delete_job_role/", views.delete_job_role, name="delete_job_role"),
    path("manage_course/", views.manage_course, name="manage_course"),
    path("edit_course/<str:id>/", views.edit_course, name="edit_course"),
    path("update_course/", views.update_course, name="update_course"),
]