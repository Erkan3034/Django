from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'image']
        labels = {
            'title': 'Başlık',
            'content': 'İçerik',
            'image': 'Görsel',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

