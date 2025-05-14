from django.contrib import admin
from django.urls import path
from article import views # Bu kod, article uygulamasındaki views.py dosyasını içe aktarır
from .import views


app_name = "article"

urlpatterns = [
    path('create/', views.index, name ="index"),
]
