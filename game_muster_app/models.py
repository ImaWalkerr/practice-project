from django.conf import settings

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class GameUser(models.Model):
    """Пользователь"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    birthday = models.DateField(verbose_name='День рождения')

    def __str__(self):
        return f"{self.user.first_name, self.user.last_name}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Test(models.Model):
    """Тест"""

    title1 = models.TextField(max_length=24, verbose_name='title_1')
    title2 = models.TextField(max_length=24, verbose_name='title_2')
    title3 = models.TextField(max_length=24, verbose_name='title_3')

    def __str__(self):
        return self.title1

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
