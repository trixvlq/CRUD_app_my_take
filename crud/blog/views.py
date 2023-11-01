from django.contrib.sessions.models import Session
from django.shortcuts import render
from django.core.cache import cache
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
    session_key = request.session.session_key
    if session_key:
        view_count_key = f'post_view_count_{post.id}_{session_key}'
        view_count = cache.get(view_count_key)
        if view_count is None:
            view_count = post.views
            cache.set(view_count_key,view_count)
            try:
                user_id = Session.objects.get(session_key=session_key).get_decoded().get('_auth_user_id')
                user = User.objects.get(id=user_id)
            except (Session.DoesNotExist,User.DoesNotExist):
                user=None
            if user is None:
                post.views += 1
                view_count = post.views
                cache.set(view_count_key,view_count,timeout="360")
                post.save()
    print(session_key)
    context = {
        "post":post
    }
    return render(request,"post.html",context)