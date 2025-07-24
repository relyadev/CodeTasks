from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.shortcuts import  redirect, render, get_object_or_404
from app.forms import RegistrationForm, EditProfileForm
from .models import UserProfile, Task, User, News, Test
from django_ratelimit.decorators import ratelimit

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
    news = News.objects.all().order_by('-date')
    context = {
        "news": news
    }
    return render(request, "main.html", context)


def tasks(request):
    tasks_list = Task.objects.all()
    return render(request, "tasks.html", {'tasks': tasks_list})


def leaders(request):
    leaders_list = UserProfile.objects.all().order_by('-points')
    total_tasks = Task.objects.count()

    context = {
        'leaders': leaders_list,
        'total_tasks': total_tasks
    }
    return render(request, "leaders.html", context)

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

    complexity_distribution = {i: all_solved_tasks.filter(complexity=i).count() for i in range(5)}

    context = {
        'profile': user_profile,
        'solved_tasks_count': solved_tasks_count,
        'last_solved_tasks': last_solved_tasks,
        'badges': badges,
        'complexity_distribution': complexity_distribution
    }

    return render(request, 'profile.html', context)
@ratelimit(key='ip', rate='1/s', block=True)

def edit_profile(req: HttpRequest):
    user = req.user
    user_profile = get_object_or_404(User, id=user.id)

    if req.method == "POST":
        form = EditProfileForm(req.POST, instance=user_profile)
        if form.is_valid():
            was_limited = getattr(req, 'limited', False)
            if was_limited:
                raise PermissionDenied("You can't edit your own profile")
            form.save()
            return redirect("profile", username=user_profile.username)
        return render(req, "profile_edit.html", {"user_profile": user_profile, "form": form})

    form = EditProfileForm(instance=user_profile)
    return render(req, "profile_edit.html", {"user_profile": user_profile, "form": form})


def ide(request: HttpRequest, task_id):
    task = get_object_or_404(Task, id=task_id)
    tests = Test.objects.filter(task=task)
    context = {
        "task": task,
        "tests": tests
    }
    return render(request, "ide.html", context)
