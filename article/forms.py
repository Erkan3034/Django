from django import forms
from .models import Article, Comment, CommunityQuestion, CommunityAnswer, Tag
from ckeditor.widgets import CKEditorWidget

#Makale formu
class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), label="İçerik")
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Etiketleri virgülle ayırarak yazınız...'}),
        help_text='Etiketleri virgülle ayırarak yazınız.'
    )
    class Meta:
        model = Article
        fields = ['title', 'content', 'image', 'category']
        labels = {
            'title': 'Başlık',
            'content': 'İçerik',
            'image': 'Görsel',
            'category': 'Kategori',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': CKEditorWidget(),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

#Yorum formu
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

#Topluluk soru formu
class CommunityQuestionForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Etiketleri virgülle ayırarak yazınız...'}),
        help_text='Etiketleri virgülle ayırarak yazınız.'
    )
    class Meta:
        model = CommunityQuestion
        fields = ['title', 'content', 'image', 'category']
        labels = {
            'title': 'Soru Başlığı',
            'content': 'Soru İçeriği',
            'image': 'Görsel',
            'category': 'Kategori',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Kısa ve açıklayıcı bir başlık...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Sorununuzu detaylıca açıklayın...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
        }

#Topluluk yanıt formu
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

