from django.shortcuts import render
from .forms import RegisterForm
from django.contrib.auth.models import User
# Create your views here.

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        newUser = User(username = username)
        newUser.set_password(password)
        newUser.save()
        
    return render(request, 'register.html', {"form": form})

def loginUser(request):
    return render(request, 'login.html')

def logoutUser(request):
    return render(request, 'logout.html')


