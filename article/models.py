from django.db import models

# Create your models here.

class Article(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE , verbose_name="Yazar")  # Bu alan, yazının yazarını (kullanıcıyı) temsil eder ve yazar silindiğinde yazıları da silinir
    title = models.CharField(max_length=50, verbose_name="Başlık") # Bu alan, yazının başlığını temsil eder ve maksimum 50 karakterlik bir metin alır
    content = models.TextField(verbose_name="İçerik") # Bu alan, yazının içeriğini temsil eder ve metin içerikleri için kullanılır
    created_date = models.DateTimeField(auto_now_add=True , verbose_name="Oluşturulma Tarihi") # Bu alan, yazının oluşturulma tarihini otomatik olarak ekler
    image = models.ImageField(upload_to='article_images/', null=True, blank=True)  # <-- yeni alan

    def __str__(self):
        return self.title # Bu kod, yazının başlığını döndürür


