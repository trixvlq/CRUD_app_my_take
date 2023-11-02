from typing import Union

from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.cache import cache

from .forms import CommentForm
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
    comments = Comment.objects.filter(post=post)
    form = CommentForm()
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
        "post":post,
        "form":form,
        "comments":comments
    }
    return render(request,"post.html",context)
def comment(request,slug):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post.objects.get(slug=slug)
            if request.user.is_authenticated:
                comment.author = request.user
            else:
                return redirect('post',slug=slug)
            comment.save()
            return redirect('home')
        else:
            return redirect('post',slug=slug)
def like(request,ident):
    user = request.user
    redirect_url = request.META.get('HTTP_REFERER', '/')
    if isinstance(ident,int):
        comment = Comment.objects.get(id=ident)
        try:
            like = Like.objects.get(comment=comment,user=user)
            like.is_active = not like.is_active
            like.save()
        except ObjectDoesNotExist:
            Like.objects.create(comment = comment,user=user,is_active=True)
    elif isinstance(ident,str):
        print("YEEEEAH BUDDY")
        post = Post.objects.get(slug=ident)
        try:
            like = Like.objects.get(post=post, user=user)
            like.is_active = not like.is_active
            like.save()
        except ObjectDoesNotExist:
            Like.objects.create(post=post, user=user, is_active=True)
        try:
            dislike = Dislike.objects.get(post=post,user=user,is_active=True)
            dislike.is_active = False
            dislike.save()
        except ObjectDoesNotExist:
            pass
    return HttpResponseRedirect(redirect_url)
def dislike(request,ident):
    user = request.user
    redirect_url = request.META.get('HTTP_REFERER', '/')
    if isinstance(ident,int):
        comment = Comment.objects.get(id=ident)
        try:
            dislike = Dislike.objects.get(comment=comment,user=user)
            dislike.is_active = not dislike.is_active
            dislike.save()
        except ObjectDoesNotExist:
            Dislike.objects.create(comment = comment,user=user,is_active=True)
    elif isinstance(ident,str):
        print("YEEEEAH BUDDY")
        post = Post.objects.get(slug=ident)
        try:
            dislike = Dislike.objects.get(post=post, user=user)
            dislike.is_active = not dislike.is_active
            print(dislike.is_active)
            dislike.save()
        except ObjectDoesNotExist:
            Dislike.objects.create(post=post, user=user, is_active=True)
        try:
            like = Like.objects.get(post=post,user=user,is_active=True)
            like.is_active = False
            like.save()
        except ObjectDoesNotExist:
            pass
    return HttpResponseRedirect(redirect_url)
