from django.shortcuts import render
from .models import *
def index(request):
    user = request.user
    Posts = Post.objects.all()
    context = {
        'posts':Posts
    }
    if not user.is_authenticated:
        return render(request,'home.html',context)
    else:
        return render(request,'base.html')