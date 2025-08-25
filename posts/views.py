from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy

from .models import Post
from .forms import PostForm, PostModelForm, CommentForm, SearchForm


class HomeView(TemplateView):
    template_name = "home.html"


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    login_url = "/login"
    paginate_by = 3  # вместо самописного кода пагинации

    def get_queryset(self):
        qs = Post.objects.exclude(author=self.request.user)
        q = self.request.GET.get("q")
        category_id = self.request.GET.get("category_id")
        tag = self.request.GET.getlist("tag")
        ordering = self.request.GET.get("orderings")

        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))
        if category_id:
            qs = qs.filter(category_id=category_id)
        if tag:
            qs = qs.filter(tags__in=tag).distinct()
        if ordering:
            qs = qs.order_by(ordering)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm(self.request.GET or None)
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"
    login_url = "/login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comments.all().order_by("-created_at")

        if self.request.method == "POST":
            form = CommentForm(self.request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = self.request.user
                comment.save()
                return redirect("post_detail", pk=post.id)
        else:
            form = CommentForm()

        context["comments"] = comments
        context["form"] = form
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_create.html"
    success_url = reverse_lazy("post_list")
    login_url = "/login"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)


class PostCreateModelFormView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostModelForm
    template_name = "posts/post_create_model_form.html"
    success_url = reverse_lazy("post_list")
    login_url = "/login"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)
