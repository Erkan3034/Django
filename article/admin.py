from django.contrib import admin

# Register your models here.

from .models import Article

admin.site.register(Article) # Bu kod, Article modelini admin panelinde görünür hale getirir
