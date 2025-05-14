from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50 , label="Kullanıcı Adı")
    password = forms.CharField(max_length=50 , label="Şifre", widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=50 , label="Şifre Doğrula", widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username") # username'i al
        password = self.cleaned_data.get("password") # password'i al
        confirm = self.cleaned_data.get("confirm") # confirm'u al
        
        if password and confirm and password != confirm:
            raise forms.ValidationError("Şifreler eşleşmiyor") # şifreler eşleşmiyorsa hata ver
        
        values = { # values'e username ve password'i at(bir sonraki sayfaya gönderilecek)
            "username": username,
            "password": password
        }
        return values
