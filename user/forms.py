from django import forms

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
