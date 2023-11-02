from django.urls import include, path
from .views import *
urlpatterns = [
    path('',index,name='home'),
    path('post/<slug:slug>/',post,name='post'),
    path('comment/<slug:slug>/',comment,name='comment'),
    path('like/<ident>/',like,name='like'),
    path('dislike/<ident>/',dislike,name='dislike'),
]