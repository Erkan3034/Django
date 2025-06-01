from django.contrib import admin
from django.urls import path
from article import views # Bu kod, article uygulamasındaki views.py dosyasını içe aktarır
from .import views
from django.contrib.auth import views as auth_views


app_name = "user"

urlpatterns = [
    path('register/', views.register, name ="register"),
    path('login/', views.loginUser, name ="login"),
    path('logout/', views.logoutUser, name ="logout"),
    path('profile/', views.profile, name="profile"),
    path('profile/edit/', views.edit_profile, name="edit_profile"),
    path('newsletter-signup/', views.newsletter_signup, name="newsletter_signup"),
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='user/password_reset.html',
             email_template_name='user/password_reset_email.html',
             subject_template_name='user/password_reset_subject.txt',
             success_url='/user/password_reset/done/'
         ), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='user/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='user/password_reset_confirm.html',
             success_url='/user/reset/done/'
         ), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='user/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
    path('<str:username>/', views.public_profile, name="public_profile"),
]
