from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Цей email вже використовується.")
        return email


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Ім`я або email')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)