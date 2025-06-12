from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

# Form untuk Registrasi User
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Form untuk Login
class CustomLoginForm(AuthenticationForm):
    pass
