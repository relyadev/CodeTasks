from django.contrib import admin
from django.urls import path, include
from app import views


urlpatterns = [
    path("", views.main, name="main"),
    path("tasks/", views.tasks, name="tasks"),
    path("ide/<int:task_id>", views.ide, name="ide"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("leaders/", views.leaders, name="leaders"),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path("submit/", views.submit, name="submit")

]
