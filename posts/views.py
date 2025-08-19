from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Post
from .forms import PostForm, PostModelForm, CommentForm


def home(request):
    return render(request, "home.html")

def test_view(request):
    return render(request, "test.html")

def post_list_view(request):
    posts = Post.objects.all()
    return render(request, "posts/post_list.html", context={"posts": posts})
    

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

def post_create_model_form_view(request):
    if request.method == 'POST':
        form = PostModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/posts')  
    else:
        form = PostModelForm()
    return render(request, 'posts/post_create_model_form.html', {'form': form})
