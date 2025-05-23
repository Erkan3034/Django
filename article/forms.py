from django import forms
from .models import Article, Comment, CommunityQuestion, CommunityAnswer
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
    parent = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    reply_to = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Comment
        fields = ['comment_content']
        labels = {
            'comment_content': 'Yorum',
        }
        widgets = {
            'comment_content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CommunityQuestionForm(forms.ModelForm):
    class Meta:
        model = CommunityQuestion
        fields = ['title', 'content', 'image']
        labels = {
            'title': 'Soru Başlığı',
            'content': 'Soru İçeriği',
            'image': 'Görsel',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kısa ve açıklayıcı bir başlık...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Sorununuzu detaylıca açıklayın...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CommunityAnswerForm(forms.ModelForm):
    class Meta:
        model = CommunityAnswer
        fields = ['content']
        labels = {
            'content': 'Yanıtınız',
        }
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Yanıtınızı yazın...'}),
        }

