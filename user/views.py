from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, UpdateView, FormView
from django.urls import reverse_lazy
import random

from .forms import RegisterForm, LoginForm
from .models import Profile
from posts.models import Post
from posts.forms import PostModelForm


class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        username = form.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            username_to_try = username + "_" + str(random.randint(0, 100))
            form.add_error("username", f"User already exists, try: {username_to_try}")
            return self.form_invalid(form)

        form.cleaned_data.pop("password_confirm")
        age = form.cleaned_data.pop("age")
        avatar = form.cleaned_data.pop("avatar")

        user = User.objects.create_user(**form.cleaned_data)
        Profile.objects.create(user=user, age=age, avatar=avatar)

        return super().form_valid(form)


class LoginView(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = authenticate(**form.cleaned_data)
        if user:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Wrong username or password")
            return self.form_invalid(form)


class LogoutView(LoginRequiredMixin, View):
    login_url = "/login"

    def get(self, request):
        logout(request)
        return redirect("home")


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"
    login_url = "/login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.request.user.profile
        posts = Post.objects.filter(author=self.request.user).order_by("-created_at")
        context.update({
            "profile": profile,
            "posts": posts
        })
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostModelForm
    template_name = "posts/post_update.html"
    success_url = reverse_lazy("profile")
    login_url = "/login"

    def get_queryset(self):
        # только посты текущего юзера
        return Post.objects.filter(author=self.request.user)
