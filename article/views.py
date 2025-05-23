from django.shortcuts import render, HttpResponse, redirect, get_object_or_404 ,reverse
from .forms import ArticleForm, CommentForm
from django.contrib import messages
from .models import Article, Comment # Bu kod, Article ve Comment modellerini import eder
from django.contrib.auth.decorators import login_required # Bu kod, kullanıcının giriş yapmış olup olmadığını kontrol eder(login_required)
from django.db import models
# Create your views here.

#================================================================
def index(request):
    articles = Article.objects.all().order_by('-created_date')[:2]  # Sadece 2 makale
    categories = [
        {"name": "Python", "url": "/category/python"},
        {"name": "Django", "url": "/category/django"},
        {"name": "Web", "url": "/category/web"},
    ]
    popular_tags = [
        {"name": "backend", "url": "/tag/backend"},
        {"name": "frontend", "url": "/tag/frontend"},
        {"name": "ai", "url": "/tag/ai"},
    ]
    context = {
        "articles": articles,
        "categories": categories,
        "popular_tags": popular_tags,
    }
    return render(request, 'index.html', context) #return HttpResponse() # Bu kod, ana sayfayı temsil eder

#================================================================
def about(request):
    return render(request, 'about.html') # Bu kod, articles.html şablonunu render eder ve döndürür
    #return HttpResponse() # Bu kod, makaleler sayfasını temsil eder

#================================================================
def detail(request, id):
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all() # Bu kod, makaleye ait tüm yorumları alır
    
    if request.method == "POST":
        comment_form = CommentForm(request.POST) # Bu kod, yorum formunu alır
        if comment_form.is_valid(): # Bu kod, formun geçerli olup olmadığını kontrol eder
            comment = comment_form.save(commit=False) # Bu kod, yorumu oluşturur
            comment.article = article # Bu kod, yorumun makalesini belirler
            comment.save() # Bu kod, yorumu kaydeder
            messages.success(request, "Yorumunuz başarıyla eklendi.")
            return redirect("article:detail", id=id )
    else:
        comment_form = CommentForm()
    
    context = {
        'article': article,
        'comments': comments, # Bu kod, makaleye ait tüm yorumları alır
        'comment_form': comment_form,
    }
    return render(request, 'detail.html', context)

#================================================================
def articles(request):
    search = request.GET.get('search')
    if search:
        # Hem başlık hem de içerikte arama yap
        articles = Article.objects.filter(
            models.Q(title__icontains=search) | 
            models.Q(content__icontains=search)
        ).order_by('-created_date')
        
        if not articles.exists():
            return render(request, 'articles.html', {'articles': [], 'search_query': search, 'featured_article': None})
        
        context = {
            'articles': articles,
            'search_query': search,  # Arama terimini template'e gönder
            'featured_article': None  # Arama yapıldığında öne çıkan makaleyi gösterme
        }
        return render(request, 'articles.html', context)
    
    # Normal sayfa görüntüleme
    articles = Article.objects.all().order_by('-created_date')
    featured_article = articles.first()
    
    context = {
        'articles': articles,
        'featured_article': featured_article,
        'search_query': None
    }
    
    return render(request, 'articles.html', context)
    

#================================================================
@login_required(login_url="user:login") #Eğer kullanıcı giriş yapmadan bu sayfaya ulaşırsa login sayfasına yönlendir
def addarticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid(): # Bu kod, formun geçerli olup olmadığını kontrol eder
        article = form.save(commit=False) # Bu kod, formu kaydetmeden önce makaleyi oluşturur
        article.author = request.user
        article.save() #Makaleyi kaydet
        messages.success(request, "Makale başarıyla oluşturuldu")
        return redirect("article:dashboard") #Makaleyi kaydettikten sonra kontrol paneline yönlendir
    return render(request, 'addarticle.html', {'form': form})

#================================================================
@login_required(login_url="user:login")
def deleteArticle(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    messages.success(request, "Makale başarıyla silindi")
    return redirect("article:dashboard")

#================================================================
@login_required(login_url="user:login")
def updateArticle(request, id):
    article = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Makale başarıyla güncellendi")
        return redirect("article:dashboard")
    return render(request, 'updatearticle.html', {'form': form})

#================================================================
#Kontrol paneli sayfası
@login_required(login_url="user:login")
def dashboard(request):
    user_articles = Article.objects.filter(author=request.user).order_by('-created_date') # Bu kod, kullanıcının yazdığı makaleleri oluşturma tarihine göre sıralar
    other_articles = Article.objects.none()
    if request.user.is_superuser or request.user.is_staff: # Bu kod, kullanıcının admin olup olmadığını kontrol eder
        other_articles = Article.objects.exclude(author=request.user).order_by('-created_date') # Bu kod, kullanıcının yazdığı makaleleri oluşturma tarihine göre sıralar
    return render(request, 'dashboard.html', { # Bu kod, kontrol paneline yönlendirir
        'user_articles': user_articles,
        'other_articles': other_articles
    })

#================================================================
#404 hatasının oluştuğu zaman açılacak olans ayfa
def handler404(request, exception):
    return render(request, '404.html', status=404)

#================================================================
def contact(request):
    return render(request, 'contact.html')

#================================================================
@login_required(login_url="user:login")
def profile(request):
    user = request.user
    articles = Article.objects.filter(author=user).order_by('-created_date')
    context = {
        'user': user,
        'articles': articles,
    }
    return render(request, 'user/profile.html', context)
#================================================================
def privacy(request):
    return render(request, 'privacy-policy.html')

#================================================================
def addcomment(request, id):
    article = get_object_or_404(Article, id=id) # makaleyi al
    if request.method == "POST": # POST isteği varsa
        comment_form = CommentForm(request.POST) # yorum formunu al
        if comment_form.is_valid(): # form geçerliyse
            comment = comment_form.save(commit=False) # yorumu oluştur
            comment.article = article
            comment.save()
            messages.success(request, "Yorumunuz başarıyla eklendi.")
            
    return redirect(reverse("article:detail", kwargs={"id": id})) #reverse fonksiyonu, URL'i ters çevirir
