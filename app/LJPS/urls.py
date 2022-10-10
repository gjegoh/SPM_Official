from django.urls import path
from . import views
from .views import SignUpView

urlpatterns = [
    path('', views.index, name='index'),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("view_job_roles/", views.view_job_roles, name="view_job_roles"),
]