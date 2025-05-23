from django.shortcuts import render, HttpResponse, redirect, get_object_or_404 ,reverse
from .forms import ArticleForm, CommentForm, CommunityQuestionForm, CommunityAnswerForm
from django.contrib import messages
from .models import Article, Comment, CommunityQuestion, CommunityAnswer # Bu kod, Article ve Comment modellerini import eder
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
    user_articles = Article.objects.filter(author=request.user).order_by('-created_date')
    other_articles = Article.objects.none()
    if request.user.is_superuser or request.user.is_staff:
        other_articles = Article.objects.exclude(author=request.user).order_by('-created_date')
    # Topluluk soruları
    if request.user.is_superuser or request.user.is_staff:
        user_questions = CommunityQuestion.objects.all().order_by('-created_date')
    else:
        user_questions = CommunityQuestion.objects.filter(user=request.user).order_by('-created_date')
    return render(request, 'dashboard.html', {
        'user_articles': user_articles,
        'other_articles': other_articles,
        'user_questions': user_questions,
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
    article = get_object_or_404(Article, id=id)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            if request.user.is_authenticated:
                comment.comment_author = request.user.get_full_name() or request.user.username
            parent_id = comment_form.cleaned_data.get('parent')
            reply_to = comment_form.cleaned_data.get('reply_to')
            if parent_id not in [None, '', 0, '0']:
                try:
                    parent_comment = Comment.objects.get(id=int(parent_id))
                    comment.parent = parent_comment
                    comment.reply_to = reply_to or parent_comment.comment_author
                except (Comment.DoesNotExist, ValueError, TypeError):
                    pass
            comment.save()
            messages.success(request, "Yorumunuz başarıyla eklendi.")
    return redirect("article:detail", id=id)

#================================================================
def sosyal(request):
    questions = CommunityQuestion.objects.all()
    return render(request, 'sosyal.html', {'questions': questions})

@login_required(login_url="user:login")
def soru_ekle(request):
    if request.method == "POST":
        form = CommunityQuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save() 
            messages.success(request, "Sorunuz topluluğa eklendi!")
            return redirect('article:sosyal')
    else:
        form = CommunityQuestionForm()
    return render(request, 'soru_ekle.html', {'form': form})

def soru_detay(request, id):
    question = get_object_or_404(CommunityQuestion, id=id)
    answers = question.answers.all()
    if request.method == "POST":
        answer_form = CommunityAnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            messages.success(request, "Yanıtınız eklendi!")
            return redirect('article:soru_detay', id=id)
    else:
        answer_form = CommunityAnswerForm()
    return render(request, 'soru_detay.html', {'question': question, 'answers': answers, 'answer_form': answer_form})

@login_required(login_url="user:login")
def soru_sil(request, id):
    question = get_object_or_404(CommunityQuestion, id=id)
    if request.user == question.user or request.user.is_superuser or request.user.is_staff:
        question.delete()
        messages.success(request, "Soru başarıyla silindi.")
    else:
        messages.error(request, "Bu soruyu silme yetkiniz yok.")
    return redirect('article:dashboard')

