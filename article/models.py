from django.db import models

# Create your models here.

class Article(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)  # Bu alan, yazının yazarını (kullanıcıyı) temsil eder ve yazar silindiğinde yazıları da silinir
    title = models.CharField(max_length=50) # Bu alan, yazının başlığını temsil eder ve maksimum 50 karakterlik bir metin alır
    content = models.TextField() # Bu alan, yazının içeriğini temsil eder ve metin içerikleri için kullanılır
    created_date = models.DateTimeField(auto_now_add=True) # Bu alan, yazının oluşturulma tarihini otomatik olarak ekler
