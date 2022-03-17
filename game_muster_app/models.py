from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class GameUser(models.Model):
    """Пользователь"""

    MALE = 'MALE'
    FEMALE = 'FEMALE'
    GENRES_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', related_name='gameuser')
    birthday = models.DateField(default=0, verbose_name='Birthday')
    gender = models.CharField(choices=GENRES_CHOICES, max_length=6, default=MALE, verbose_name='Gender')
    age = models.IntegerField(default=0, verbose_name='Age')
    email_verify = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name, self.user.last_name}"

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
