from datetime import timedelta

from django.conf import settings
from django.db import models

from users.models import NULLABLE


class Habit(models.Model):

    PERIODICITY_CHOICES = (
        (0, 'Daily'),
        (1, 'Every Monday'),
        (2, 'Every Tuesday'),
        (3, 'Every Wednesday'),
        (4, 'Every Thursday'),
        (5, 'Every Friday'),
        (6, 'Every Saturday'),
        (7, 'Every Sunday'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE)
    action = models.TextField()
    place = models.CharField(max_length=100, verbose_name='Place to action')
    time = models.TimeField(**NULLABLE, verbose_name='Time to action')
    duration = models.DurationField(default=timedelta(minutes=2), verbose_name='Duration of action')
    periodicity = models.CharField(max_length=1, choices=PERIODICITY_CHOICES, default='0',
                                   verbose_name='Periodicity of action')
    reward = models.CharField(max_length=100, **NULLABLE)
    related_action = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Related action', **NULLABLE)
    is_pleasant = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner} - {self.action}'

    class Meta:
        verbose_name = 'Habit'
        verbose_name_plural = 'Habits'
