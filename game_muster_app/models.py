from django.contrib.auth.models import AbstractUser
from django.db import models


class GameUser(AbstractUser):
    """
    Extension for model user
    """
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    GENRES_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]

    birthday = models.DateField(default=0, verbose_name='Birthday')
    gender = models.CharField(choices=GENRES_CHOICES, max_length=6, default=MALE, verbose_name='Gender')
    email_verify = models.BooleanField(default=False, verbose_name='Email verification status')

    def __str__(self):
        return f"{self.first_name, self.last_name}"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class UserFavoriteGames(models.Model):
    """
    User wishlist
    """
    owner = models.ForeignKey(GameUser, on_delete=models.CASCADE, verbose_name='Owner', related_name='owner_favorites')
    game_id = models.ForeignKey(
        'Games', on_delete=models.CASCADE, verbose_name='User games', related_name='user_favorite_games'
    )

    def __str__(self):
        return f"{self.owner}"

    class Meta:
        db_table = 'user_wishlist'
        verbose_name = 'User wishlist'
        verbose_name_plural = 'Users wishlists'


class Platforms(models.Model):
    """
    Platforms model
    """
    platform_id = models.IntegerField(default=0, verbose_name='Platform id')
    platform_name = models.CharField(max_length=124, verbose_name='Platform name')

    def __str__(self):
        return f"{self.platform_name}"

    class Meta:
        db_table = 'platforms'
        verbose_name = 'Platform'
        verbose_name_plural = 'Platforms'


class Genres(models.Model):
    """
    Genres model
    """
    genre_id = models.IntegerField(default=0, verbose_name='Genre id')
    genre_name = models.CharField(max_length=124, verbose_name='Genre name')

    def __str__(self):
        return f"{self.genre_name}"

    class Meta:
        db_table = 'genres'
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Games(models.Model):
    """
    Games model
    """
    game_id = models.IntegerField(unique=True, default=0, verbose_name='Game Id from Igdb.com')
    game_name = models.CharField(max_length=124, verbose_name='Game name')
    game_summary = models.TextField(null=True, max_length=1024, verbose_name='Game summary')
    game_genres = models.ManyToManyField(
        Genres, verbose_name='Game genres', related_name='game_genres'
    )
    game_platforms = models.ManyToManyField(
        Platforms, verbose_name='Game platforms', related_name='game_platforms'
    )
    cover_url = models.CharField(null=True, max_length=256, verbose_name='Game cover')
    release_dates = models.CharField(null=True, max_length=124, verbose_name='Game release dates')
    rating = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, default=None, verbose_name='Game rating'
    )
    rating_count = models.IntegerField(null=True, default=None, verbose_name='Game rating count')
    aggregated_rating = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, default=None, verbose_name='Game aggregated rating'
    )
    aggregated_rating_count = models.IntegerField(
        null=True, default=None, verbose_name='Game aggregated rating count'
    )
    favorite_games = models.ManyToManyField(
        GameUser, through='UserFavoriteGames', verbose_name='game_in_users_favorites',
        related_name='game_in_users_favorites'
    )

    def __str__(self):
        return f"{self.game_name}"

    class Meta:
        db_table = 'games'
        verbose_name = 'Games catalog'
        verbose_name_plural = 'Games catalogs'


class ScreenShots(models.Model):
    """
    Screenshots model
    """
    game = models.ForeignKey(Games, on_delete=models.CASCADE, verbose_name='Game', related_name='game_screenshots')
    screenshot_url = models.CharField(null=True, max_length=256, verbose_name='Game screenshot')

    def __str__(self):
        return f"{self.game}"

    class Meta:
        db_table = 'screenshots'
        verbose_name = 'Screenshot'
        verbose_name_plural = 'Screenshots'
