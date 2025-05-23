from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class Article(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE , verbose_name="Yazar")  # Bu alan, yazının yazarını (kullanıcıyı) temsil eder ve yazar silindiğinde yazıları da silinir
    title = models.CharField(max_length=50, verbose_name="Başlık") # Bu alan, yazının başlığını temsil eder ve maksimum 50 karakterlik bir metin alır
    content = RichTextField(verbose_name="İçerik") # Bu alan, yazının içeriğini temsil eder ve metin içerikleri için kullanılır
    created_date = models.DateTimeField(auto_now_add=True , verbose_name="Oluşturulma Tarihi") # Bu alan, yazının oluşturulma tarihini otomatik olarak ekler
    image = models.ImageField(upload_to='article_images/', null=True, blank=True)  # <-- yeni alan

    def __str__(self):
        return self.title # Bu kod, yazının başlığını döndürür
    
    class Meta:
        ordering = ['-created_date'] # Bu kod, yazıları tarihe göre sıralar


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Makale", related_name="comments")
    comment_author = models.CharField(max_length=50, verbose_name="İsim")
    comment_content = models.TextField(max_length=200, verbose_name="Yorum")
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_content # Bu kod, yorumun içeriğini döndürür
    
    class Meta:
        ordering = ['-comment_date'] # Bu kod, yorumları tarihe göre sıralar


