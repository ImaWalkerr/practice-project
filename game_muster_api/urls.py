from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'games', GamesViewSet, basename='games')
router.register(r'genres', GenresViewSet, basename='genres')
router.register(r'platforms', PlatformsViewSet, basename='platforms')
router.register(r'screenshots', ScreenShotsViewSet, basename='screenshots')
router.register(r'favorite_games', UserFavoriteGamesViewSet, basename='favorite_games')


urlpatterns = [
    path('v1/drf-auth/', include('rest_framework.urls')),
    path('v1/', include(router.urls)),
]
