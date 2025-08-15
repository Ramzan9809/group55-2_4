from django.shortcuts import render
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate


def register_view(request):
    form = RegisterForm()
    return render(request, 'users/register.html', context={'form': form})



def login_view(request):
    form = LoginForm()
    return render(request, 'users/login.html', context={'form': form})