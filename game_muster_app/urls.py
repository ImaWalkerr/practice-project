from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('<int:game_id>/', GamesDetailPageView.as_view(), name='games_detail_page'),
    path('sign_up_page/', RegistrationView.as_view(), name='sign_up_page'),
    path('log_in_page/', LoginView.as_view(), name='log_in_page'),
    path('logout', do_logout, name='logout'),
    ]
