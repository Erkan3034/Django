from django.contrib import admin
from .models import Profile, NewsletterEmail

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'github']
    search_fields = ['user__username', 'github']
    list_filter = ['user__is_active']

@admin.register(NewsletterEmail)
class NewsletterEmailAdmin(admin.ModelAdmin):
    list_display = ['email', 'created']
    search_fields = ['email']
    list_filter = ['created']
