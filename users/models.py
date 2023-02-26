from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """ User class """
    email = models.EmailField(
        'Email',
        unique=True,
        max_length=50,
    )
    username = models.CharField(
        'Username',
        unique=True,
        max_length=50,
    )
    first_name = models.CharField(
        'Name',
        max_length=50,
    )
    last_name = models.CharField(
        'Last name',
        max_length=50,
    )
    password = models.CharField(
        'Password',
        max_length=255,
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
