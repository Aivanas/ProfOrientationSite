from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from StudyPlatform.models import CustomUser


class LoginForm(AuthenticationForm):
    email = forms.EmailField(label="Адрес электронной почты", widget=forms.EmailInput())
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    remember_me = forms.BooleanField(required=False, initial=False)



class RegisterUserForm(UserCreationForm):
    email = forms.CharField(label='Электронная почта', widget=forms.TextInput(attrs={'class': "form-input"}))
    id_first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': "form-input"}))
    id_last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': "form-input"}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': "form-input"}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': "form-input"}))

    class Meta:
        model = CustomUser
        fields = ('id_first_name', 'id_last_name', 'email', 'password1', 'password2')
        widgets = {
            'id_first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'id_last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'})
        }
        field_order = ['id_first_name', 'id_last_name', 'email', 'password1', 'password2']
