from random import random

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
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

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

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




