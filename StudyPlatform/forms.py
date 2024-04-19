from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from StudyPlatform.models import User


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class LoginForm(AuthenticationForm):
    username = None
    email = forms.EmailInput()
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    remember_me = forms.BooleanField(required=False, initial=False)
    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)


class RegisterUserForm(UserCreationForm):
    email = forms.CharField(label='Электронная почта', widget=forms.TextInput(attrs={'class': "form-input"}))
    id_first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': "form-input"}))
    id_last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': "form-input"}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': "form-input"}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': "form-input"}))

    class Meta:
        model = User
        fields = ('id_first_name', 'id_last_name', 'email', 'password1', 'password2')
        widgets = {
            'id_first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'id_last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'})
        }
        field_order = ['id_first_name', 'id_last_name', 'email', 'password1', 'password2']
