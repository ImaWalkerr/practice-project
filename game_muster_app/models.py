from django.db import models


class Images(models.Model):
    """
    Тех изображения
    """

    info_image = models.CharField(max_length=255, verbose_name='Описание')
    image = models.ImageField(verbose_name='Изображение', upload_to='images')

    def __str__(self):
        return str(self.info_image)

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'


class ScreenShots(models.Model):
    """
    Скриншоты
    """

    info_image = models.CharField(max_length=255, verbose_name='Описание')
    screenshots = models.ImageField(verbose_name='Скриншоты', upload_to='screenshots')

    def __str__(self):
        return str(self.info_image)

    class Meta:
        verbose_name = 'Скриншот'
        verbose_name_plural = 'Скриншоты'


class Games(models.Model):
    """
    Игры
    """

    ARCADE = 'arcade'
    ACTION = 'action'
    STRATEGY = 'strategy'
    SPORT = 'sport'
    ADVENTURE = 'adventure'
    RPG = 'rpg'

    GENRE_CHOICES = (
        (ARCADE, 'Аркада'),
        (ACTION, 'Экшн'),
        (STRATEGY, 'Стратегия'),
        (SPORT, 'Спорт'),
        (ADVENTURE, 'Приключения'),
        (RPG, 'Ролевые')
    )

    image = models.ImageField(verbose_name='Постер игры', upload_to='games')
    name = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(max_length=1024, verbose_name='Об игре')
    release_date = models.CharField(max_length=255, verbose_name='Дата выхода')
    ratings = models.ManyToManyField("Ratings")
    genres = models.CharField(max_length=255, verbose_name='Жанр', choices=GENRE_CHOICES, default=ARCADE)
    platforms = models.CharField(max_length=255, verbose_name='Платформы')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'


class Ratings(models.Model):
    """
    Рейтинги
    """

    users = models.FloatField(default=0, verbose_name='Оценка пользователей')
    critics = models.FloatField(default=0, verbose_name='Оценка критиков')
    users_count = models.IntegerField(default=0, verbose_name='Кол-во оценок пользователей')
    critics_count = models.IntegerField(default=0, verbose_name='Кол-во оценок критиков')

    def __str__(self):
        return str(self.users)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
