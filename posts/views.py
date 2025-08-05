from django.shortcuts import render, HttpResponse
import random
from .models import Post


def home(request):
    return render(request, "base.html")

def test_view(request):
    return HttpResponse("World hello!")

def post_list_view(request):
    posts = Post.objects.all()
    return render(request, "post_list.html", context={"posts": posts})