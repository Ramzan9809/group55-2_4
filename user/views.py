from django.shortcuts import render, redirect
import random
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "users/register.html", context={"form": form})
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return render(request, "users/register.html", context={"form": form})
        else:
            username = form.cleaned_data["username"]
            if User.objects.filter(username=username).exists():
                username_to_try = username + "_" + str(random.randint(0, 100))
                form.add_error("username", f"User already exists, try: {username_to_try}")
                return render(request, "users/register.html", context={"form": form})

            form.cleaned_data.pop("password_confirm")

            user = User.objects.create_user(**form.cleaned_data)

            login(request, user)

            return redirect("home")


def login_view(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request, "users/login.html", context={"form": form})
    if request.method == "POST":
        form = LoginForm(request.POST)
        if not form.is_valid():
            return render(request=request, template_name="users/login.html", context={"form": form})
        elif form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user:
                login(request, user)
                return redirect("home")
            elif not user:
                form.add_error(None, "Wrong username or password")
                return render(request=request, template_name="users/login.html", context={"form": form})


@login_required(login_url="/login")
def logout_view(request):
    if request.method == "GET":
        logout(request)
        return redirect("home")
