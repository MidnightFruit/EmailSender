from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    USERNAME_FIELD = 'email'
    company_name = models.CharField(max_length=100, verbose_name="Название компании")
    email = models.EmailField(unique=True, verbose_name='Почта', null=False, blank=False)
    phone = models.CharField(max_length=11, verbose_name='телефон', null=True, blank=True)
    country = models.CharField(max_length=25, verbose_name='Страна', null=True, blank=True)
    token = models.CharField(max_length=255, verbose_name="Токен", blank=True, null=True)

    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        permissions = [
            ('can_block_users', 'can block users'),
            ('can_view_list_of_users', 'can view list of users')
        ]

    def __str__(self):
        return self.email
