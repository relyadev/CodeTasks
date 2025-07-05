from django.contrib import admin
from django.urls import path, include
from app import views
urlpatterns = [
    path("", views.main, name="main"),
    path("tasks/", views.tasks, name="tasks"),
    path("profile/", views.profile, name="profile"),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),

]
