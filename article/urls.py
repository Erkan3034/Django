from django.contrib import admin
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "article"

urlpatterns = [
    path('/index', views.index, name="index"),
    path('', views.articles, name="articles"), # Bu kod, makaleler sayfasını temsil eder ve articles fonksiyonunu çağırır
    path('dashboard/', views.dashboard, name="dashboard"), # Bu kod, kontrol paneli sayfasını temsil eder ve dashboard fonksiyonunu çağırır
    path('addarticle/', views.addarticle, name="addarticle"), # Bu kod, makale ekleme sayfasını temsil eder ve addarticle fonksiyonunu çağırır
    path('detail/<int:id>/', views.detail, name="detail"), # Bu kod, makale detay sayfasını temsil eder ve detail fonksiyonunu çağırır
    path('delete/<int:id>/', views.deleteArticle, name="delete"), # Bu kod, makale silme sayfasını temsil eder ve delete fonksiyonunu çağırır
    path('update/<int:id>/', views.updateArticle, name="update"), # Bu kod, makale güncelleme sayfasını temsil eder ve update fonksiyonunu çağırır
    path('comment/<int:id>', views.addcomment, name="comment"), # Bu kod, yorum ekleme sayfasını temsil eder ve addcomment fonksiyonunu çağırır
    # --- Sosyal (Topluluk) ---
    path('sosyal/', views.sosyal, name="sosyal"),
    path('sosyal/soru-ekle/', views.soru_ekle, name="soru_ekle"),
    path('sosyal/soru/<int:id>/', views.soru_detay, name="soru_detay"),
    path('sosyal/soru-sil/<int:id>/', views.soru_sil, name="soru_sil"),
]
