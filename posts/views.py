from django.shortcuts import render, HttpResponse
from .models import Post


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