from django.urls import path
from .views import *

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('<int:game_id>/', GamesDetailPageView.as_view(), name='games_detail_page'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('my_must/', MyFavoritesView.as_view(), name='my_must'),
    path('error_search/', ErrorSearchView.as_view(), name='error_search'),
    path('sign_up_page/', RegistrationView.as_view(), name='sign_up_page'),
    path('login_page/', LoginView.as_view(), name='login_page'),
    path('logout/', do_logout, name='logout'),
    path('logout_done/', LogoutDoneView.as_view(), name='logout_done'),
    path('invalid_verify/', InvalidVerifyView.as_view(), name='invalid_verify'),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),
    path('confirm_email/', ConfirmEmailView.as_view(), name='confirm_email'),
    path('add/', add_to_favorites, name='add_to_favorites'),
    path('remove/', remove_from_favorites, name='remove_from_favorites'),
    path('delete/', delete_favorites, name='delete_favorites'),
    path('api/', favorites_api, name='favorites_api'),
    ]

