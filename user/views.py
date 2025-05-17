from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User # kullanıcı modeli 
from django.contrib.auth import login, authenticate, logout # login, authenticate, logout fonksiyonları
# Create your views here.

def register(request):
        form = RegisterForm(request.POST or None) # form'u oluştur(post request için)
        if form.is_valid(): # form'un doğru mu yanlış mı olduğunu kontrol et(forms.py dekiclean metodu ile)
            username = form.cleaned_data.get("username") # username'i al
            password = form.cleaned_data.get("password") # password'i al
            newUser = User(username = username) # yeni kullanıcı oluştur
            newUser.set_password(password) # password'i ayarla
            newUser.save() # kullanıcıyı kaydet

            login(request, newUser) # kullanıcıyı login et
            return redirect("index") # index sayfasına yönlendir
        else:
            form = RegisterForm()  # GET isteğinde form'u burda oluşturman gerekiyor

        return render(request, 'register.html', {"form": form})

def loginUser(request):
    return render(request, 'login.html')

def logoutUser(request):
    return render(request, 'logout.html')


