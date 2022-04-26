from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .permissions import IsAdminOrReadOnly
from .serializers import *


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly, )


class PlatformsViewSet(viewsets.ModelViewSet):
    queryset = Platforms.objects.all()
    serializer_class = PlatformsSerializer
    permission_classes = (IsAdminOrReadOnly, )


class ScreenShotsViewSet(viewsets.ModelViewSet):
    queryset = ScreenShots.objects.all()
    serializer_class = ScreenshotSerializer
    permission_classes = (IsAdminOrReadOnly, )


class GamesViewSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


class GamesViewSet(viewsets.ModelViewSet):
    queryset = Games.objects.all()
    serializer_class = GamesSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = GamesViewSetPagination


class UserFavoriteGamesViewSet(viewsets.ModelViewSet):
    queryset = UserFavoriteGames.objects.all()
    serializer_class = UserFavoriteGamesSerializer
    permission_classes = (IsAdminOrReadOnly, )
