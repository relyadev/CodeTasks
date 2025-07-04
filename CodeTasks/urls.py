from django.contrib import admin
from django.urls import path, include
from app import views
import django.contrib.auth.urls
urlpatterns = [
    path("", views.main, name="main"),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),

]
