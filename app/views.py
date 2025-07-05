from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from app.forms import RegistrationForm
from .models import UserProfile, Task

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

@login_required
def main(request):
    return render(request, "main.html")

@login_required
def tasks(request):
    return render(request, "tasks.html")

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    all_solved_tasks = user_profile.tasks.all()
    solved_tasks_count = all_solved_tasks.count()
    last_solved_tasks = all_solved_tasks.order_by('-id')[:3]
    total_tasks = Task.objects.count()
    badges = user_profile.bages.all()

    context = {
        'profile': user_profile,
        'solved_tasks_count': solved_tasks_count,
        'last_solved_tasks': last_solved_tasks,
        'total_tasks': total_tasks,
        'badges': badges,
        'complexity_distribution': {
            1: 5,
            2: 10,
            3: 7,
            4: 3,
            5: 1
        }
    }
    return render(request, 'profile.html', context)