from django.contrib import admin
from .models import *


@admin.register(Images)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'info_image',
                    'image')
    list_display_links = ('info_image',)


@admin.register(ScreenShots)
class ScreenShotsAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'info_image',
                    'screenshots')
    list_display_links = ('info_image',)


@admin.register(Games)
class GamesAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'name',
                    'description',
                    'release_date',
                    'genres',
                    'platforms')
    list_display_links = ('name',)


@admin.register(Ratings)
class RatingsAdmin(admin.ModelAdmin):
    list_display = ('id',
                    'users',
                    'critics',
                    'users_count',
                    'critics_count')
    list_display_links = ('id',)


