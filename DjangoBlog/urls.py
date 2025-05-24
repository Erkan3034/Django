"""
URL configuration for DjangoBlog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from article import views # Bu kod, article uygulamasındaki views.py dosyasını içe aktarır
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name ="index"), # Bu kod, ana sayfayı temsil eder ve index fonksiyonunu çağırır
    path('about/', views.about, name ="about"), # Bu kod, makaleler sayfasını temsil eder ve about fonksiyonunu çağırır
    
    path('articles/', include('article.urls')), # Bu kod, makaleler sayfasını temsil eder ve article.urls dosyasını içe aktarır
    
    path('detail/<int:id>', views.detail, name ="detail"), # Bu kod, makaleler sayfasınının detayını temsil eder ve detail fonksiyonunu çağırır

    path('user/', include('user.urls')), # Bu kod, kullanıcı sayfasını temsil eder ve user.urls dosyasını içe aktarır

    path('contact/', views.contact, name ="contact"), # Bu kod, iletişim sayfasını temsil eder ve contact fonksiyonunu çağırır

    path('profile/', views.profile, name ="profile"), # Bu kod, profil sayfasını temsil eder ve profil fonksiyonunu çağırır
    path('privacy-policy/', views.privacy, name ="privacy"), # Bu kod, privacy sayfasını temsil eder ve search fonksiyonunu çağırır

    path('sosyal/', views.sosyal, name ="sosyal"), # Bu kod, sosyal sayfasını temsil eder ve sosyal fonksiyonunu çağırır

    path('search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('search_suggestions/', views.search_suggestions),  # opsiyonel, ikisi de çalışsın diye

    path('chatbot/', include('chatbot.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
