from django.shortcuts import render
from .models import *
def index(request):
    user = request.user
    Posts = Post.objects.all()
    context = {
        'posts':Posts
    }
    if not user.is_authenticated:
        print('user is not authenticated')
        return render(request,'home.html',context)
    else:
        return render(request,'home.html',context)
def post(request,slug):
    post = Post.objects.get(slug=slug)
    context = {
        "post":post
    }
    return render(request,"post.html",context)