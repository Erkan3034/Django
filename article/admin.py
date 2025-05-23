from django.contrib import admin

# Register your models here.

from .models import Article, Comment , Category, Tag


admin.site.register(Comment) # admin panelinde Comment modelini görüntülemek/özelleştirmek için kullanılır
admin.site.register(Category)
admin.site.register(Tag)

@admin.register(Article) # admin panelinde Article modelini görüntülemek/özelleştirmek için kullanılır
class ArticleAdmin(admin.ModelAdmin): # admin panelinde Article modelini görüntülemek/özelleştirmek için kullanılır
    list_display = ["title", "author", "created_date"] #Listede bunlarda göüzkür
    list_display_links = ["title", "created_date"] # title ve created_date link oalrak article'a yönlendirsin.
    search_fields = ["title", "content"] # arama kutusunda title ve content içeriği aranır
    list_filter = ["created_date"] #Liste larak oluşturulam atarihlerne öre çerikleri sıralar
    
    class Meta:
        model = Article
    


