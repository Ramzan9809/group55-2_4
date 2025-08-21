from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm, PostModelForm, CommentForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def home(request):
    return render(request, "home.html")


@login_required(login_url="/login")
def post_list_view(request):
    limit = 3
    posts = Post.objects.all()
    form = SearchForm(request.GET or None)
    q = request.GET.get("q")
    category_id = request.GET.get("category_id")
    tag = request.GET.getlist("tag")
    ordering = request.GET.get("orderings")
    page = int(request.GET.get("page", 1))
    if q:
        posts = posts.filter(Q(title__icontains=q) | Q(content__icontains=q))
    if category_id:
        posts = posts.filter(category_id=category_id)
    if tag:
        posts = posts.filter(tags__in=tag).distinct()
    if ordering:
        posts = posts.order_by(ordering)
    if page:
        max_page = len(posts) / limit
        if round(max_page) < max_page:
            max_page = round(max_page) + 1
        else:
            max_page = round(max_page)
        start = (page - 1) * limit
        end = start * limit
        posts = posts[start:end]
    return render(request, "posts/post_list.html", context={"posts": posts, "form": form, "max_page": range(1, max_page + 1)})  


@login_required(login_url="/login")
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by("-created_at")

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect("post_detail", post_id=post.id)
        else:
            return redirect("login")
    else:
        form = CommentForm()

    return render(request, "posts/post_detail.html", {
        "post": post,
        "comments": comments,
        "form": form,
    })


@login_required(login_url="/login")
def post_create_view(request):
    if request.method == "GET":
        form = PostForm()
        return render(request, "posts/post_create.html", context={"form": form})
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, "posts/post_create.html", context={"form": form})
        else:
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            img = form.cleaned_data.get("img")
            Post.objects.create(title=title, content=content, img=img)
    return redirect("/posts")


@login_required(login_url="/login")
def post_create_model_form_view(request):
    if request.method == 'POST':
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/posts')  
    else:
        form = PostModelForm()
    return render(request, 'posts/post_create_model_form.html', {'form': form})

