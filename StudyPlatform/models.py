from random import random

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class User(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        ("Логин"),
        max_length=150,
        unique=True,
        help_text=(
            "Обязательное для ввода поле. Только буквы, цифры и символы @/./+/-/_ "
        ),
        validators=[username_validator],
        error_messages={
            "unique": ("Пользователь с таким логином уже существует"),
        },
    )
    first_name = models.CharField(("Имя"), max_length=150, blank=True)
    last_name = models.CharField(("Фамилия"), max_length=150, blank=True)
    email = models.EmailField(("адрес электронной почты"), blank=True)
    is_staff = models.BooleanField(
        ("Статус персонала"),
        default=False,
        help_text=("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        ("активен"),
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(("дата регистрации"), default=timezone.now)

    #objects = UserManager()
    #EMAIL_FIELD = "email"
    #USERNAME_FIELD = "username"
    #REQUIRED_FIELDS = ["email"]


    class Meta(AbstractUser.Meta):
        verbose_name = ("Пользователь")
        verbose_name_plural = ("Пользователи")
        swappable = "AUTH_USER_MODEL"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

class Test(models.Model):
    name = models.CharField(max_length=255, unique=True)
    test_type = models.CharField(max_length=50, choices=[('psychological', 'Психологический'), ('personality', 'Личностный'), ('educational', 'Образовательный')])

class Question(models.Model):
    QUESTION_TYPES = [
        ('single_choice', 'Одиночный выбор'),
        ('multiple_choice', 'Множественный выбор'),
        # Добавьте другие типы вопросов здесь
    ]
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=255)
    choice_image = models.ImageField(upload_to='choices/', blank=True)
    is_correct = models.BooleanField(default=False)


class UserTests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userTestsUser")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="userTestTest")
    is_done = models.BooleanField(default=False)


class UserTestAnswers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userAnswersUser")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="userAnswerTest")
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name="userAnswerChoice")