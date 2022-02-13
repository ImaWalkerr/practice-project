from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page, name='main_page'),
    path('games_detail_page', games_detail_page, name='games_detail_page'),
    ]
