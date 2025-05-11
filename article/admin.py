from django.contrib import admin

# Register your models here.

from .models import Article

@admin.register(Article) # admin panelinde Article modelini görüntülemek/özelleştirmek için kullanılır
class ArticleAdmin(admin.ModelAdmin): # admin panelinde Article modelini görüntülemek/özelleştirmek için kullanılır
    list_display = ["title", "author", "created_date"]
    list_display_links = ["title", "created_date"]
    search_fields = ["title", "content"]
    list_filter = ["created_date"]
    
    class Meta:
        model = Article
    


