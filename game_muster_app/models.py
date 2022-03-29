from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class GameUser(models.Model):
    """
    Extension for model user
    """
    MALE = 'MALE'
    FEMALE = 'FEMALE'
    GENRES_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='User', related_name='game_user')
    birthday = models.DateField(default=0, verbose_name='Birthday')
    gender = models.CharField(choices=GENRES_CHOICES, max_length=6, default=MALE, verbose_name='Gender')
    age = models.IntegerField(default=0, verbose_name='Age')
    email_verify = models.BooleanField(default=False, verbose_name='Email verification status')

    def __str__(self):
        return f"{self.user.first_name, self.user.last_name}"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Platforms(models.Model):
    """
    Platforms model
    """
    name = models.CharField(max_length=124)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = 'Platform'
        verbose_name_plural = 'Platforms'


class Genres(models.Model):
    """
    Genres model
    """
    name = models.CharField(max_length=124)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'


class Games(models.Model):
    """
    Games catalog
    """
    game_id = models.IntegerField(default=0, verbose_name='Game Id from Igdb.com')
    game_name = models.CharField(max_length=124, verbose_name='Game name')
    game_summary = models.TextField(max_length=1024, verbose_name='Game summary')
    game_genres = models.ManyToManyField(Genres, verbose_name='Game genres')
    game_platforms = models.ManyToManyField(Platforms, verbose_name='Game platforms')
    cover = models.CharField(max_length=256, verbose_name='Game cover')
    release_dates = models.DateTimeField(null=True, default=None)
    rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, default=None)
    rating_count = models.IntegerField(null=True, default=None)
    aggregated_rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, default=None)
    aggregated_rating_count = models.IntegerField(null=True, default=None)
    must = models.BooleanField(default=False)
    # favorite_games = models.ManyToManyField(User, through="UserFavoriteGames")

    def __str__(self):
        return f"{self.game_name}"

    class Meta:
        ordering = ["game_name"]
        verbose_name = 'Games catalog'
        verbose_name_plural = 'Games catalogs'


class ScreenShots(models.Model):
    """
    Screenshots model
    """
    game = models.ForeignKey(Games, on_delete=models.CASCADE, verbose_name='Game', related_name='game_screenshots')
    screenshot_url = models.CharField(max_length=256, verbose_name='Game screenshot')

    def __str__(self):
        return f"{self.game}"

    class Meta:
        verbose_name = 'ScreenShot'
        verbose_name_plural = 'ScreenShots'


class UserFavoriteGames(models.Model):
    """
    User wishlist
    """
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Owner', related_name='user_favorite_game')
    # games = models.ForeignKey(Games, on_delete=models.CASCADE, verbose_name='User games', related_name='user_games')

    def __str__(self):
        return f"{self.owner}"

    class Meta:
        verbose_name = 'User wishlist'
        verbose_name_plural = 'Users wishlists'
