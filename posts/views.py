from django.shortcuts import render, HttpResponse
import random


def test_view(request):
    return HttpResponse("World hello!")

def html_view(request):
    return render(request, "base.html")