from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django_ratelimit.decorators import ratelimit
import requests
from app.forms import RegistrationForm, EditProfileForm
from .models import UserProfile, User, News, Test, Task, Language, Solution


def handler404(request, exception):
    return render(request, "errors/404.html", status=404)


def handler403(request, exception):
    return render(request, "errors/403.html", status=403)


def register(req: HttpRequest):
    if req.method == "POST":
        form = RegistrationForm(req.POST, req.FILES)
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
    news = News.objects.all().order_by("-date")
    context = {"news": news}
    return render(request, "main.html", context)


def tasks(request):
    tasks_list = Task.objects.all()
    return render(request, "tasks.html", {"tasks": tasks_list})


def leaders(request):
    leaders_list = UserProfile.objects.all().order_by("-points")
    total_tasks = Task.objects.count()

    context = {"leaders": leaders_list, "total_tasks": total_tasks}
    return render(request, "leaders.html", context)


def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user__username=username)
    all_solved_tasks = Task.objects.filter(
        solution__user=user, solution__is_solved=True
    ).distinct()

    solved_tasks_count = all_solved_tasks.count()
    last_solved_tasks = all_solved_tasks.order_by("-solution__date_solution")[:3]
    badges = user_profile.badges.all()
    complexity_distribution = {
        i: all_solved_tasks.filter(complexity=i).count() for i in range(5)
    }

    context = {
        "profile": user_profile,
        "solved_tasks_count": solved_tasks_count,
        "last_solved_tasks": last_solved_tasks,
        "badges": badges,
        "complexity_distribution": complexity_distribution,
    }

    return render(request, "profile.html", context)


@ratelimit(key="ip", rate="1/s", block=True)
def edit_profile(req: HttpRequest):
    user = req.user
    user_profile = get_object_or_404(User, id=user.id)

    if req.method == "POST":
        form = EditProfileForm(req.POST, instance=user_profile)
        if form.is_valid():
            was_limited = getattr(req, "limited", False)
            if was_limited:
                raise PermissionDenied("You can't edit your own profile")
            form.save()
            return redirect("profile", username=user_profile.username)
        return render(
            req, "profile_edit.html", {"user_profile": user_profile, "form": form}
        )

    form = EditProfileForm(instance=user_profile)
    return render(
        req, "profile_edit.html", {"user_profile": user_profile, "form": form}
    )


def ide(request: HttpRequest, task_id):
    task = get_object_or_404(Task, id=task_id)
    tests = Test.objects.filter(task=task)
    languages = Language.objects.all()
    context = {"task": task, "tests": tests, "languages": languages}

    return render(request, "ide.html", context)


import json

def submit(req: HttpRequest):
    if req.method != "POST":
        return HttpResponse("Method not allowed", status=405)

    data = json.loads(req.body)
    task_id = data.get("task_id")
    source_code = data.get("source_code")
    language_id = data.get("language")

    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return HttpResponse("Task not found", status=404)

    try:
        language = Language.objects.get(language=language_id)
    except Language.DoesNotExist:
        return HttpResponse("Invalid language", status=400)

    existing_solution = Solution.objects.filter(
        task=task,
        user=req.user,
        language=language,
        is_solved=True
    ).first()

    if existing_solution:
        return JsonResponse({"result": "already_solved", "message": "You've already solved this task"})

    solution = Solution.objects.create(
        task=task,
        language=language,
        code=source_code,
        user=req.user
    )

    url = "https://judge0-ce.p.rapidapi.com/submissions/batch?base64_encoded=false&wait=true&fields=*"

    payload = {
        "submissions": [
            {
                "language_id": language_id,
                "source_code": source_code,
                "stdin": test.stdin,
                "expected_output": test.stdout,
            }
            for test in task.test_set.all()
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
        "x-rapidapi-key": "b1de749e9amsh9617460bd0bb4b8p137f54jsn0f18f135190c",
    }

    try:
        resp = requests.post(url, json=payload, headers=headers)
        resp.raise_for_status()
        resp_data = resp.json()

        tokens = ",".join(item["token"] for item in resp_data)
        check_url = f"https://judge0-ce.p.rapidapi.com/submissions/batch?tokens={tokens}&base64_encoded=false&fields=status"

        result = requests.get(check_url, headers=headers)
        result.raise_for_status()
        result_data = result.json()

        is_solved = all(s["status"]["id"] == 3 for s in result_data.get("submissions", []))

        solution.is_solved = is_solved
        solution.save()
        user_profile = UserProfile.objects.get(user=req.user)
        user_profile.points += task.award_points
        user_profile.save()

        return JsonResponse({"result": "yes" if is_solved else "no"})

    except requests.RequestException as e:
        return HttpResponse(f"Error connecting to Judge0: {str(e)}", status=500)
