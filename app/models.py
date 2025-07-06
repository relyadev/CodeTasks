from django.db import models
from django.contrib.auth.models import User

class Badge(models.Model):
    name = models.CharField(max_length=100)
    COLOR_CHOICES = [
        (0, "Green"),
        (1, "Blue"),
        (2, "Yellow"),
        (3, "Purple"),
        (4, "Red"),
    ]
    color = models.IntegerField(choices=COLOR_CHOICES)

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    COMPLEXITY_CHOICES = [
        (0, 'Easy'),
        (1, 'Medium'),
        (2, 'Hard'),
        (3, "Extreme"),
        (4, "Hardcore")
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
    badges = models.ManyToManyField(Badge, blank=True)

    def __str__(self):
        return f"UserProfile for {self.user.username}"

class Solution(models.Model):
    LANGUAGE_CHOICES = [
        ('python', "Python"),
        ('java', "Java"),
        ('c++', "C++"),
        ('c#', "C#"),
        ('javascript', "JavaScript"),
        ('pascal', "Pascal")
    ]

    language = models.CharField(
        max_length=20,
        choices=LANGUAGE_CHOICES,
        default='python'
    )
    code = models.TextField()
    is_solved = models.BooleanField(default=False)
    date_solution = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='solutions')

    def __str__(self):
        return f"Solution for {self.task.title} by {self.user.username}"
    