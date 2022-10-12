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
]