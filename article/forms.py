from django import forms
from .models import Article
from ckeditor.widgets import CKEditorWidget

class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), label="İçerik")
    class Meta:
        model = Article
        fields = ['title', 'content', 'image']
        labels = {
            'title': 'Başlık',
            'image': 'Görsel',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

