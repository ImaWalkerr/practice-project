from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('<int:game_id>/', GamesDetailPageView.as_view(), name='games_detail_page'),
    ]
