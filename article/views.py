from django.shortcuts import render, HttpResponse, redirect, get_object_or_404 ,reverse
from .forms import ArticleForm, CommentForm, CommunityQuestionForm, CommunityAnswerForm
from django.contrib import messages
from .models import Article, Comment, CommunityQuestion, CommunityAnswer, Category, Tag # Bu kod, Article ve Comment modellerini import eder
from django.contrib.auth.decorators import login_required # Bu kod, kullanıcının giriş yapmış olup olmadığını kontrol eder(login_required)
from django.db import models
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from user.forms import NewsletterForm
# Create your views here.

#================================================================
def index(request):
    articles = Article.objects.all().order_by('-created_date')[:6] # Bu kod, tüm makaleleri oluşturma tarihine göre sıralar ve ilk 6 makaleyi alır
    all_categories = list(Category.objects.all())
    main_categories = all_categories[:3]
    other_categories = all_categories[3:]
    popular_tags = Tag.objects.all()[:6]  # En popüler 6 etiketi göstermek için (isteğe göre değiştirilebilir)
    recent_questions = CommunityQuestion.objects.all().order_by('-created_date')[:3]
    User = get_user_model()
    site_stats = {
        'total_articles': Article.objects.count(),
        'total_comments': Comment.objects.count(),
        'total_questions': CommunityQuestion.objects.count(),
        'total_users': User.objects.count(),
    }
    top_authors = User.objects.annotate(article_count=models.Count('article')).order_by('-article_count', 'username')[:3]
    context = {
        "articles": articles,
        "main_categories": main_categories,
        "other_categories": other_categories,
        "popular_tags": popular_tags,
        "recent_questions": recent_questions,
        "site_stats": site_stats,
        "top_authors": top_authors,
        "NewsletterForm": NewsletterForm(),
    }
    return render(request, 'index.html', context)

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
    category_id = request.GET.get('category')
    tag_name = request.GET.get('tag')
    articles = Article.objects.all().order_by('-created_date')
    if category_id:
        articles = articles.filter(category_id=category_id)
    if tag_name:
        articles = articles.filter(tags__name=tag_name)
    if search:
        articles = articles.filter(
            models.Q(title__icontains=search) | 
            models.Q(content__icontains=search)
        ).order_by('-created_date')
        if not articles.exists():
            return render(request, 'articles.html', {'articles': [], 'search_query': search, 'featured_article': None, 'categories': Category.objects.all()})
        context = {
            'articles': articles,
            'search_query': search,
            'featured_article': None,
            'categories': Category.objects.all(),
        }
        return render(request, 'articles.html', context)
    featured_article = articles.first()
    context = {
        'articles': articles,
        'featured_article': featured_article,
        'search_query': None,
        'categories': Category.objects.all(),
    }
    return render(request, 'articles.html', context)
    

#================================================================
@login_required(login_url="user:login")
def addarticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        # Etiketleri işle
        tags_str = form.cleaned_data.get('tags', '')
        if tags_str:
            tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
            tag_objs = []
            for name in tag_names:
                tag, created = Tag.objects.get_or_create(name=name)
                tag_objs.append(tag)
            article.tags.set(tag_objs)
        form.save_m2m()
        messages.success(request, "Makale başarıyla oluşturuldu")
        return redirect("article:dashboard")
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
@login_required(login_url="user:login")
def addcomment(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
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
    category_id = request.GET.get('category')
    questions = CommunityQuestion.objects.all()
    if category_id:
        questions = questions.filter(category_id=category_id)
    categories = Category.objects.all()
    return render(request, 'sosyal.html', {'questions': questions, 'categories': categories})

@login_required(login_url="user:login")
def soru_ekle(request):
    if request.method == "POST":
        form = CommunityQuestionForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            # Etiketleri işle
            tags_str = form.cleaned_data.get('tags', '')
            if tags_str:
                tag_names = [t.strip() for t in tags_str.split(',') if t.strip()]
                tag_objs = []
                for name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=name)
                    tag_objs.append(tag)
                question.tags.set(tag_objs)
            form.save_m2m()
            messages.success(request, "Sorunuz topluluğa eklendi!")
            return redirect('article:sosyal')
    else:
        form = CommunityQuestionForm()
    return render(request, 'soru_ekle.html', {'form': form})

def soru_detay(request, id):
    question = get_object_or_404(CommunityQuestion, id=id)
    answers = question.answers.all()
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.warning(request, "Yanıt vermek için giriş yapmalısınız.")
            return redirect(f'/user/login/?next={request.path}')
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

def search_suggestions(request):
    query = request.GET.get('q', '').strip()
    results = []
    if query:
        articles = Article.objects.filter(title__icontains=query)[:5]
        questions = CommunityQuestion.objects.filter(title__icontains=query)[:5]
        for a in articles:
            results.append({
                'type': 'blog',
                'id': a.id,
                'title': a.title,
                'url': f'/articles/detail/{a.id}' # Bu kod, makale sayfasının detayını temsil eder
            })
        for q in questions:
            results.append({
                'type': 'sosyal',
                'id': q.id,
                'title': q.title,
                'url': f'/articles/sosyal/soru/{q.id}' # Bu kod, sosyal sayfasının soru detayını temsil eder
            }) 
    return JsonResponse({'results': results})

