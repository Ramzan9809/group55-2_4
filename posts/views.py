from django.shortcuts import render, HttpResponse, redirect
from .models import Post
from .forms import PostForm, PostModelForm


def home(request):
    return render(request, "home.html")

def test_view(request):
    return render(request, "test.html")

def post_list_view(request):
    posts = Post.objects.all()
    return render(request, "posts/post_list.html", context={"posts": posts})
    
def post_detail(request, post_id):
    posts = Post.objects.get(id=post_id)
    return render(request, "posts/post_detail.html", context={"posts": posts})

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
