from django.conf import settings

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Пользователь"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    birthday = models.DateField(verbose_name='День рождения')

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
