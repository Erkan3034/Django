from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'github']
    search_fields = ['user__username', 'github']
    list_filter = ['user__is_active']
