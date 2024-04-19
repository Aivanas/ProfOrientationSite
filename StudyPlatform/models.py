from random import random

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.text import slugify


class User(AbstractUser):
    email = models.EmailField("адрес электронной почты", blank=False, unique=True, null=False)
    REQUIRED_FIELDS = ['email']


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        username = slugify(email)[:30]
        while self.model.objects.filter(username=username).exists():
            username = slugify(email + str(random.randint(100, 999)))[:30]
        user.username = username
        user.save(using=self._db)
        return user

    def authenticate(self, email=None, password=None):
        try:
            user = self.model._default_manager.get(email=email)
        except self.model.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
            else:
                return None
