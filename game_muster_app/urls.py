from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('<int:game_id>/', GamesDetailPageView.as_view(), name='games_detail_page'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('my_must/', MyFavoritesView.as_view(), name='my_favorites'),
    path('anonym_must/', FavoritesAnonymView.as_view(), name='anonym_favorites'),
    path('search_error/', ErrorSearchView.as_view(), name='search_error'),
    path('sign_up_page/', RegistrationView.as_view(), name='sign_up_page'),
    path('login_page/', LoginView.as_view(), name='login_page'),
    path('logout/', do_logout, name='logout'),
    path('logout_done/', LogoutDoneView.as_view(), name='logout_done'),
    path('invalid_verify/', InvalidVerifyView.as_view(), name='invalid_verify'),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),
    path('confirm_email/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('<int:game_id>/add_to_favorites', add_to_favorites, name='add_to_favorites'),
    path('<int:game_id>/remove_from_favorites', remove_from_favorites, name='remove_from_favorites'),
    ]
