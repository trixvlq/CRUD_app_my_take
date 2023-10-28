from django.shortcuts import render

def index(request):
    user = request.user
    if user.is_authenticated:
        return render(request,'home.html')
    else:
        return render(request,'base.html')