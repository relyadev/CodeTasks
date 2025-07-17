from django.contrib import admin
from app.models import Task, Test, UserProfile, Solution, Badge, News

admin.site.register(Test)
admin.site.register(Task)
admin.site.register(UserProfile)
admin.site.register(Solution)
admin.site.register(Badge)
admin.site.register(News)