from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='email',
        help_text='please provide your email'
    )
    name = models.CharField(
        max_length=150,
        verbose_name='name',
        help_text='please provide your name'
    )
    surname = models.CharField(
        max_length=150,
        verbose_name='surname',
        help_text='please provide your surname'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'surname']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('username',)

    def __str__(self):
        return self.username