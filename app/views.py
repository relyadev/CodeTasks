from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from app.forms import RegistrationForm
from .models import UserProfile

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
    return render(request, "base.html")