from django import forms
from .models import Article, Comment
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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_author', 'comment_content']
        labels = {
            'comment_author': 'İsim',
            'comment_content': 'Yorum',
        }
        widgets = {
            'comment_author': forms.TextInput(attrs={'class': 'form-control'}),
            'comment_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

