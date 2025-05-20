from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User # kullanıcı modeli 
from django.contrib.auth import login, authenticate, logout # login, authenticate, logout fonksiyonları
from django.db import IntegrityError
from django.contrib import messages # flashmesajları göstermek için





# Create your views here.

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        try:
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            github = form.cleaned_data.get("github")

            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'Bu kullanıcı adı zaten kullanılıyor.')
                return render(request, 'register.html', {"form": form})
            
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'Bu e-posta adresi zaten kullanılıyor.')
                return render(request, 'register.html', {"form": form})

            # Create new user
            newUser = User(username=username, email=email)
            newUser.set_password(password)
            newUser.save()

            # Save github profile if provided
            if github:
                newUser.profile.github = github
                newUser.profile.save()
        
            login(request, newUser)
            messages.success(request, "Kayıt başarılı! Hoş geldiniz, giriş yaptınız.")
            return redirect("index")
        except IntegrityError:
            form.add_error(None, 'Kayıt işlemi sırasında bir hata oluştu. Lütfen tekrar deneyin.')
    return render(request, 'register.html', {"form": form})

# Login View
def loginUser(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(request, username=username, password=password) # kullanıcı doğrulama 
        if user is not None:
            login(request, user) # kullanıcı giriş yap 
            messages.success(request, "Giriş yapıldı. Hoş geldiniz.")
            return redirect("index")
        else:
            messages.info(request, "Kullanıcı adı veya şifre hatalı.")
            return render(request, 'login.html', {"form": form})
        
    return render(request, 'login.html', {"form": form}) # login sayfasını render et eğer form geçerli değilse

def logoutUser(request):
    logout(request)
    messages.success(request, "Başarıyla çıkış yapıldı!")
    return redirect("index")


