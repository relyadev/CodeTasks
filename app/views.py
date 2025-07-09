from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import  redirect, render, get_object_or_404
from app.forms import RegistrationForm
from .models import UserProfile, Task, User

def handler404(request, exception):
    return render(request, "errors/404.html", status=404)

def handler403(request, exception):
    return render(request, "errors/403.html", status=403)

def register(req: HttpRequest):
    if req.method == "POST":
        form = RegistrationForm(req.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            UserProfile.objects.create(user=user)
            return redirect("login")
        else:
            return render(req, "registration/registration.html", {"form": form})

    form = RegistrationForm()
    return render(req, "registration/registration.html", {"form": form})

def main(request):
    return render(request, "main.html")

def tasks(request):
    return render(request, "tasks.html")

def leaders(request):
    return render(request, "leaders.html")


def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user__username=username)

    all_solved_tasks = Task.objects.filter(
        solution__user=user,
        solution__is_solved=True
    ).distinct()

    solved_tasks_count = all_solved_tasks.count()
    last_solved_tasks = all_solved_tasks.order_by('-solution__date_solution')[:3]
    badges = user_profile.badges.all()

    complexity_distribution = {
        0: all_solved_tasks.filter(complexity=0).count(),
        1: all_solved_tasks.filter(complexity=1).count(),
        2: all_solved_tasks.filter(complexity=2).count(),
        3: all_solved_tasks.filter(complexity=3).count(),
        4: all_solved_tasks.filter(complexity=4).count()
    }

    context = {
        'profile': user_profile,
        'solved_tasks_count': solved_tasks_count,
        'last_solved_tasks': last_solved_tasks,
        'badges': badges,
        'complexity_distribution': complexity_distribution
    }

    return render(request, 'profile.html', context)



