from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from game_muster_app.models import *


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'


class PlatformsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platforms
        fields = '__all__'


class ScreenshotSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScreenShots
        fields = '__all__'


class GenresForGamesSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'


class PlatformsForGamesSerializer(PrimaryKeyRelatedField, serializers.ModelSerializer):
    class Meta:
        model = Platforms
        fields = '__all__'


class GamesSerializer(serializers.ModelSerializer):
    game_platforms = PlatformsForGamesSerializer(many=True, queryset=Genres.objects.all())
    game_genres = GenresForGamesSerializer(many=True, queryset=Platforms.objects.all())

    class Meta:
        model = Games
        fields = '__all__'


class UserFavoriteGamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserFavoriteGames
        fields = '__all__'
