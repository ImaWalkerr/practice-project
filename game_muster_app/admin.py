from django.contrib import admin
from .models import *


@admin.register(GameUser)
class GameUserAdmin(admin.ModelAdmin):
    fields = (
        ('user', 'birthday', 'gender'), 'email_verify'
    )
    list_display = ('user', 'email_verify')
    list_display_links = ('user',)


@admin.register(UserFavoriteGames)
class UserFavoriteGamesAdmin(admin.ModelAdmin):
    fields = ('owner', 'game_id')
    list_display = ('owner', 'game_id')
    list_display_links = ('owner',)


@admin.register(Platforms)
class PlatformsAdmin(admin.ModelAdmin):
    fields = ('platform_id', 'platform_name')
    list_display = ('platform_id', 'platform_name')
    list_display_links = ('platform_name',)


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    fields = ('genre_id', 'genre_name')
    list_display = ('genre_id', 'genre_name')
    list_display_links = ('genre_name',)


@admin.register(Games)
class GamesAdmin(admin.ModelAdmin):
    fields = (
        ('game_id', 'game_name', 'release_dates'), 'game_summary', ('game_genres', 'game_platforms'), 'cover_url',
        ('rating', 'rating_count', 'aggregated_rating', 'aggregated_rating_count')
    )
    list_display = ('game_id', 'game_name')
    list_display_links = ('game_name',)


@admin.register(ScreenShots)
class ScreenShotsAdmin(admin.ModelAdmin):
    fields = ('game', 'screenshot_url')
    list_display = ('game', 'screenshot_url')
    list_display_links = ('game',)
