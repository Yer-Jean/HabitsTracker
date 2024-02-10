from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None  # удаляем поле username, так как авторизовать будем по полю email
    email = models.EmailField(unique=True, verbose_name='Email')

    first_name = models.CharField(max_length=50, verbose_name='Name', **NULLABLE)
    last_name = models.CharField(max_length=50, verbose_name='Surname', **NULLABLE)
    telegram_name = models.CharField(max_length=50, verbose_name='Telegram username', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ('email',)

    def __str__(self):
        return f'{self.email}'
