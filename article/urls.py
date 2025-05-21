from django.contrib import admin
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static


app_name = "article"

urlpatterns = [
    path('create/', views.index, name="index"),
    path('', views.articles, name="articles"), # Bu kod, makaleler sayfasını temsil eder ve articles fonksiyonunu çağırır
    path('dashboard/', views.dashboard, name="dashboard"), # Bu kod, kontrol paneli sayfasını temsil eder ve dashboard fonksiyonunu çağırır
    path('addarticle/', views.addarticle, name="addarticle"), # Bu kod, makale ekleme sayfasını temsil eder ve addarticle fonksiyonunu çağırır
    path('detail/<int:id>/', views.detail, name="detail"), # Bu kod, makale detay sayfasını temsil eder ve detail fonksiyonunu çağırır
]
