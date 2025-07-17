from django.contrib import admin
from django.urls import path, include
from app import views
import subprocess


urlpatterns = [
    path("", views.main, name="main"),
    path("tasks/", views.tasks, name="tasks"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("leaders/", views.leaders, name="leaders"),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),

]
