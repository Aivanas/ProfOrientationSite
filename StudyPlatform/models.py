from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(("email address"), blank=False, unique=True, null=False)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
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