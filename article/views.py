from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .forms import ArticleForm
from django.contrib import messages
from .models import Article
from django.contrib.auth.decorators import login_required
# Create your views here.

#================================================================
def index(request):
    context = {
        "number1": 10,
        "number2": 20,
        "number3": 30,
    }
    return render(request, 'index.html' , context) # Bu kod, index.html şablonunu render eder ve döndürür
    #return HttpResponse() # Bu kod, ana sayfayı temsil eder

#================================================================
def about(request):
    return render(request, 'about.html') # Bu kod, articles.html şablonunu render eder ve döndürür
    #return HttpResponse() # Bu kod, makaleler sayfasını temsil eder

#================================================================
def detail(request, id): # Bu kod, makale detay sayfasını temsil eder ve detail fonksiyonunu çağırır
    article = get_object_or_404(Article, id=id)  # Bu kod, makaleyi alır ve id'ye göre filtreler eğer id yoksa 404 hatası döner
    return render(request, 'detail.html', {'article': article})

#================================================================
def create(request):
    return HttpResponse("Yazı Oluştur")

#================================================================
def articles(request):
    articles = Article.objects.all().order_by('-created_date')  # En yeniden eskiye sırala
    featured_article = articles.first()  # İlk makaleyi öne çıkan olarak al
    
    context = {
        'articles': articles,
        'featured_article': featured_article
    }
    
    return render(request, 'articles.html', context)
    

#================================================================
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
def deleteArticle(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    messages.success(request, "Makale başarıyla silindi")
    return redirect("article:dashboard")

#================================================================
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
@login_required
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
