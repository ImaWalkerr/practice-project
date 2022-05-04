from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination

from .permissions import IsAdminOrReadOnly
from .serializers import *


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['genre_name']


class PlatformsViewSet(viewsets.ModelViewSet):
    queryset = Platforms.objects.all()
    serializer_class = PlatformsSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['platform_name']


class ScreenShotsViewSet(viewsets.ModelViewSet):
    queryset = ScreenShots.objects.all()
    serializer_class = ScreenshotSerializer
    permission_classes = (IsAdminOrReadOnly, )


class GamesViewSetPagination(PageNumberPagination):
    page_size = 500
    page_size_query_param = 'page_size'
    max_page_size = 1000


class GamesViewSet(viewsets.ModelViewSet):
    queryset = Games.objects.all()
    serializer_class = GamesSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = GamesViewSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['game_name']
    ordering_fields = ['game_name']


class UserFavoriteGamesViewSet(viewsets.ModelViewSet):
    queryset = UserFavoriteGames.objects.all()
    serializer_class = UserFavoriteGamesSerializer
    permission_classes = (IsAdminOrReadOnly, )
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['owner_id']
