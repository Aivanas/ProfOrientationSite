from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import capfirst

from StudyPlatform.models import User, Question, Test, Choice, UserTests


#Question


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True}), label="Логин")
    password = forms.CharField(
        label=("Пароль"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': "form-input"}))  # Добавлено поле для логина
    email = forms.CharField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': "form-input"}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': "form-input"}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': "form-input"}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': "form-input"}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': "form-input"}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')  # Логин добавлен в список полей
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        }
        field_order = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']  # Логин первым

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким логином уже существует.")
        return username


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['name', 'test_type']
    def clean_name(self):
        name = self.cleaned_data.get("name")
        if Test.objects.filter(name=name).exists():
            raise forms.ValidationError("Тест с таким названием уже существует")
        return name

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'question_type']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text', 'choice_image', 'is_correct']


class UserTestForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label="Пользователь")
    test = forms.ModelChoiceField(queryset=Test.objects.all(), label="Тест")

    class Meta:
        model = UserTests
        fields = ['user', 'test']