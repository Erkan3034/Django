from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, LoginForm, ProfileEditForm, NewsletterForm
from django.contrib.auth.models import User # kullanıcı modeli 
from django.contrib.auth import login, authenticate, logout # login, authenticate, logout fonksiyonları
from django.db import IntegrityError
from django.contrib import messages # flashmesajları göstermek için
from django.contrib.auth.decorators import login_required
from article.models import Article, CommunityQuestion
from .models import Profile, NewsletterEmail





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

def dashboard(request):
    return render(request, 'dashboard.html')

@login_required(login_url="login")
def profile(request):
    user = request.user
    articles = Article.objects.filter(author=user).order_by('-created_date')
    context = {
        'user': user,
        'articles': articles,
    }
    return render(request, 'user/profile.html', context)

@login_required(login_url="login")
def edit_profile(request):
    user = request.user
    profile = user.profile
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            profile.save()
            messages.success(request, "Profiliniz başarıyla güncellendi.")
            return redirect('user:profile')
    else:
        form = ProfileEditForm(instance=profile, initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        })
    return render(request, 'user/edit_profile.html', {'form': form})


def public_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    articles = Article.objects.filter(author=user).order_by('-created_date')
    questions = CommunityQuestion.objects.filter(user=user).order_by('-created_date')
    context = {
        'profile_user': user,
        'profile': profile,
        'articles': articles,
        'questions': questions,
    }
    return render(request, 'user/public_profile.html', context)

def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not NewsletterEmail.objects.filter(email=email).exists():
                form.save()
                messages.success(request, 'Tebrikler Bültenimize başarıyla abone oldun! Bizden her zaman ilk sen haberdar olacaksın!')
            else:
                messages.info(request, 'Bu e-posta zaten bültenimize kayıtlı. Geçerli bir e-posta adresi girmeye ne dersin?')
        else:
            messages.error(request, 'Bomm, Geçersiz bir e-posta adresi girdin. Geçerli bir e-posta adresi girmeye ne dersin?')
        return redirect('index')
    else:
        return redirect('index')
