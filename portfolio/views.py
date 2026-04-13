from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "portfolio/index.html")


def detail(request):
    return render(request, "blog/blog-detail.html")