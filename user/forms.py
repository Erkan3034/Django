from django import forms
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label="Kullanıcı Adı")
    password = forms.CharField(
        max_length=50, 
        label="Şifre", 
        widget=forms.PasswordInput
    )


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, label="Kullanıcı Adı")
    email = forms.EmailField(label="E-posta")  # Otomatik geçerlilik kontrolü yapılır
    github = forms.URLField(label="Github Profil Linki", required=False)  # Opsiyonel

    password = forms.CharField(
        max_length=50, 
        label="Şifre", 
        widget=forms.PasswordInput
    )
    confirm = forms.CharField(
        max_length=50, 
        label="Şifre Doğrula", 
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm")
        github = cleaned_data.get("github")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Şifreler eşleşmiyor!") #password confirm

        if github and not github.startswith("https://github.com/"):
            raise forms.ValidationError("Geçerli bir Github linki girin (https://github.com/...)")

        return cleaned_data


class ProfileEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label="Ad")
    last_name = forms.CharField(max_length=30, required=False, label="Soyad")
    email = forms.EmailField(required=True, label="E-posta")
    class Meta:
        model = Profile
        fields = ['image', 'bio', 'github']
        labels = {
            'image': 'Profil Fotoğrafı',
            'bio': 'Biyografi',
            'github': 'Github',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Kendinizi kısaca tanıtın...'}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Github profil linkiniz...'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
