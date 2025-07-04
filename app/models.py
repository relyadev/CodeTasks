from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    COMPLEXITY_CHOICES = [
        (1, 'Easy'),
        (2, 'Medium'),
        (3, 'Hard'),
        (4, "Extreme"),
        (5, "Hardcore")
    ]
    complexity = models.IntegerField(choices=COMPLEXITY_CHOICES)
    award_points = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Test(models.Model):
    stdin = models.TextField()
    stdout = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"Test for {self.task.title}"

class UserProfile(models.Model):
    resolved_task_count = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tasks = models.ManyToManyField(Task, blank=True)

    def __str__(self):
        return f"UserProfile for {self.user.username}"
