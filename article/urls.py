from django.contrib import admin
from django.urls import path
from article import views # Bu kod, article uygulamasındaki views.py dosyasını içe aktarır
from .import views


app_name = "article"

urlpatterns = [
    path('create/', views.index, name="index"),
    path('', views.articles, name="articles"), # Bu kod, makaleler sayfasını temsil eder ve articles fonksiyonunu çağırır
    path('dashboard/', views.dashboard, name="dashboard"), # Bu kod, kontrol paneli sayfasını temsil eder ve dashboard fonksiyonunu çağırır
]
