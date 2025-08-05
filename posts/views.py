from django.shortcuts import render, HttpResponse
from .models import Post


def home(request):
    return render(request, "home.html")

def test_view(request):
    return render(request, "test.html")

def post_list_view(request):
    posts = Post.objects.all()
    return render(request, "post_list.html", context={"posts": posts})