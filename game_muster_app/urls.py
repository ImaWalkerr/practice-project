from django.urls import path
from .views import *

urlpatterns = [
    path('', main_page, name='main_page'),
    path('<int:game_id>/', games_detail_page, name='games_detail_page'),
    ]
