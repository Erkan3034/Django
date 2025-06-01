from django.contrib import admin
from django.urls import path
from article import views # Bu kod, article uygulamasındaki views.py dosyasını içe aktarır
from .import views


app_name = "user"

urlpatterns = [
    path('register/', views.register, name ="register"),
    path('login/', views.loginUser, name ="login"),
    path('logout/', views.logoutUser, name ="logout"),
    path('profile/', views.profile, name="profile"),
    path('profile/edit/', views.edit_profile, name="edit_profile"),
    path('newsletter-signup/', views.newsletter_signup, name="newsletter_signup"),
    path('<str:username>/', views.public_profile, name="public_profile"),
]
