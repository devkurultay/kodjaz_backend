from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.urls import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, password, email, **kwargs):
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, email, **kwargs):
        user = self.create_user(
            email=email,
            password = password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    email = models.EmailField(_('email address'), blank=True, unique=True)

    def __str__(self):
        return '{} {}'.format(self.username, self.email)

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'name': self.name})

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
