from django.contrib import admin
from django.urls import path
from article import views # Bu kod, article uygulamasındaki views.py dosyasını içe aktarır
from .import views


app_name = "user"

urlpatterns = [
    path('register/', views.register, name ="register"),
    path('login/', views.loginUser, name ="login"),
    path('logout/', views.logoutUser, name ="logout"),
]
