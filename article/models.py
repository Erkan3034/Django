from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model

# Create your models here.

class Article(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE , verbose_name="Yazar")  # Bu alan, yazının yazarını (kullanıcıyı) temsil eder ve yazar silindiğinde yazıları da silinir
    title = models.CharField(max_length=50, verbose_name="Başlık") # Bu alan, yazının başlığını temsil eder ve maksimum 50 karakterlik bir metin alır
    content = RichTextField(verbose_name="İçerik") # Bu alan, yazının içeriğini temsil eder ve metin içerikleri için kullanılır
    created_date = models.DateTimeField(auto_now_add=True , verbose_name="Oluşturulma Tarihi") # Bu alan, yazının oluşturulma tarihini otomatik olarak ekler
    image = models.ImageField(upload_to='article_images/', null=True, blank=True)  # <-- yeni alan
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name="articles", verbose_name="Kategori")
    tags = models.ManyToManyField('Tag', blank=True, related_name="articles", verbose_name="Etiketler")

    def __str__(self):
        return self.title # Bu kod, yazının başlığını döndürür
    
    class Meta:
        ordering = ['-created_date'] # Bu kod, yazıları tarihe göre sıralar


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Makale", related_name="comments")
    comment_author = models.CharField(max_length=50, verbose_name="İsim")
    comment_content = models.TextField(max_length=200, verbose_name="Yorum")
    comment_date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies', verbose_name="Yanıtlanan Yorum")
    reply_to = models.CharField(max_length=50, null=True, blank=True, verbose_name="Yanıtlanan Kullanıcı")

    def __str__(self):
        return self.comment_content # Bu kod, yorumun içeriğini döndürür
    
    class Meta:
        ordering = ['-comment_date'] # Bu kod, yorumları tarihe göre sıralar
        
#================================================================

class CommunityQuestion(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Soran Kullanıcı", related_name="community_questions")
    title = models.CharField(max_length=200, verbose_name="Soru Başlığı")
    content = models.TextField(verbose_name="Soru İçeriği")
    image = models.ImageField(upload_to='community_images/', null=True, blank=True, verbose_name="Görsel")
    created_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name="community_questions", verbose_name="Kategori")
    tags = models.ManyToManyField('Tag', blank=True, related_name="community_questions", verbose_name="Etiketler")

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-created_date']

class CommunityAnswer(models.Model):
    question = models.ForeignKey(CommunityQuestion, on_delete=models.CASCADE, related_name="answers", verbose_name="Soru")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Yanıtlayan Kullanıcı", related_name="community_answers")
    content = models.TextField(verbose_name="Yanıt")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Yanıt: {self.content[:30]}..."
    class Meta:
        ordering = ['created_date']

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Kategori Adı")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ['name']

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Etiket")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Etiket"
        verbose_name_plural = "Etiketler"
        ordering = ['name']


