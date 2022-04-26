from django import views
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.http import urlsafe_base64_decode
from django.views.generic.base import TemplateView

from game_muster_app.api.igdb_wrapper import IGDB_WRAPPER
from .models import *
from .forms import LoginForm, RegistrationForm
from game_muster_app.api.twitter_wrapper import TWITTER_WRAPPER
from game_muster_app.tasks import refresh_games
from .utils import send_email_for_verify


class BasePageView(TemplateView):
    template_name = 'base.html'

    def get(self, *args, **kwargs):
        users = GameUser.objects.all()

        context = {
            'users': users
        }

        return context


def get_list_of_filters(option, data_from_filter):
    """
    Return list of values from data_from_filter
    """
    return list(map(int, data_from_filter.getlist(option)))


class MainPageView(views.View):
    """
    Functional for main page
    """
    def get(self, request):

        # celery_task = refresh_games.delay()

        data_from_filter = request.GET
        igdb_search = request.GET.get('search_game')
        platform_id = request.GET.getlist('platform_id')
        genre_id = request.GET.getlist('genre_id')
        ratings_min = request.GET.get('min')
        ratings_max = request.GET.get('max')

        chosen_params = {'platform_id': platform_id, 'genre_id': genre_id, 'rating': (ratings_min, ratings_max)}

        if 'platform_id' in data_from_filter:
            chosen_params['platform_id'] = get_list_of_filters('platform_id', data_from_filter)

        if 'genre_id' in data_from_filter:
            chosen_params['genre_id'] = get_list_of_filters('genre_id', data_from_filter)

        if 'rating' in data_from_filter:
            chosen_params['rating'] = data_from_filter['rating']

        genres_main = Genres.objects.all().distinct('genre_name')
        platforms_main = Platforms.objects.all().distinct('platform_name')

        try:
            if igdb_search:
                games_main = Games.objects.filter(game_name__icontains=igdb_search)
            else:
                games_main = Games.objects.all()

            if not games_main:
                raise LookupError
        except LookupError:
            return redirect('search_error')

        if chosen_params['platform_id']:
            games_main = games_main.filter(game_platforms__platform_id__in=chosen_params['platform_id'])

        if chosen_params['genre_id']:
            games_main = games_main.filter(game_genres__genre_id__in=chosen_params['genre_id'])

        if 'rating' in chosen_params['rating']:
            games_main = games_main.filter(
                rating__gte=chosen_params['rating'][0], rating__lte=chosen_params['rating'][1]
            )
        else:
            games_main = Games.objects.all()

        paginator = Paginator(games_main, 6)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        num_of_pages = "a" * page_obj.paginator.num_pages

        context = {
            'games_main': games_main,
            'genres_main': genres_main,
            'platforms_main': platforms_main,
            'favorite_game_list_ids': favorite_game_list_ids(request),
            'page_obj': page_obj,
            'num_of_pages': num_of_pages,
            'platforms_chosen': chosen_params['platform_id'],
            'genres_chosen': chosen_params['genre_id'],
            'rating': chosen_params['rating'],
            'title': 'GameMuster',
        }

        return render(request, 'main_page.html', context)


class ErrorSearchView(TemplateView):
    template_name = 'search_error.html'


class GamesDetailPageView(views.View):
    """
    Functional for current game page
    """
    def get(self, request, game_id):

        current_game = Games.objects.filter(game_id=game_id)
        current_game_for_tweets = Games.objects.get(game_id=game_id)
        game_name = current_game_for_tweets.game_name
        tweets_for_current_game = TWITTER_WRAPPER.get_tweets_for_game(game_name)
        screenshots = ScreenShots.objects.all()
        genres_main = Genres.objects.all()
        platforms_main = Platforms.objects.all()

        context = {
            'current_game': current_game,
            'screenshots': screenshots,
            'genres_main': genres_main,
            'tweets_for_current_game': tweets_for_current_game,
            'platforms_main': platforms_main,
            'favorite_game_list_ids': favorite_game_list_ids(request),
            'title': 'Game details',
        }
        return render(request, 'games_detail_page.html', context)


class ProfileView(views.View):

    def get(self, request):
        users = GameUser.objects.first()
        context = {
            'users': users,
            'title': 'Profile',
        }

        return render(request, 'registration/profile_page.html', context)


class LoginView(views.View):

    def get(self, request):
        form = LoginForm(request.POST or None)
        context = {
            'form': form,
            'title': 'Login',
        }
        return render(request, 'registration/login_page.html', context)

    def post(self, request):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
        context = {
            'form': form,
            'title': 'Login',
        }
        return render(request, 'registration/login_page.html', context)


class RegistrationView(views.View):

    def get(self, request):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form,
            'title': 'Registration',
        }
        return render(request, 'registration/sign_up_page.html', context)

    def post(self, request):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.set_password(form.cleaned_data['password'])
            GameUser.objects.create(
                birthday=form.cleaned_data['birthday'],
                gender=form.cleaned_data['gender'],
            )
            new_user.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            send_email_for_verify(request, user)
            return redirect('confirm_email')
        context = {
            'form': form,
            'title': 'Registration',
        }
        return render(request, 'registration/sign_up_page.html', context)


class EmailVerify(views.View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect('/')
        return redirect('invalid_verify')

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = GameUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                GameUser.DoesNotExist, ValidationError):
            user = None
        return user


class InvalidVerifyView(TemplateView):
    template_name = 'registration/invalid_verify.html'


class ConfirmEmailView(TemplateView):
    template_name = 'registration/confirm_email.html'


def do_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('logout_done')
    else:
        return HttpResponse(f'You must login first!')


class LogoutDoneView(TemplateView):
    template_name = 'registration/logout_done.html'


class MyFavoritesView(views.View):

    def get(self, request):

        favorites_list = (
            [favorite_games for favorite_games in UserFavoriteGames.objects.filter(owner=request.user)]
            if request.user.is_authenticated
            else []
        )

        favorite_games = [
            favorite_game.game_id
            for favorite_game in UserFavoriteGames.objects.filter(owner=request.user)
        ]

        paginator = Paginator(favorite_games, 12)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        num_of_pages = "a" * page_obj.paginator.num_pages

        context = {
            'favorites_list': favorites_list,
            'favorite_games': favorite_games,
            'favorite_game_list_ids': favorite_game_list_ids(request),
            'page_obj': page_obj,
            'num_of_pages': num_of_pages,
            'title': 'My favorites',
        }
        if request.user.is_authenticated:
            return render(request, 'favorites/favorites_page.html', context)
        else:
            return render(request, 'favorites/favorites_for_anonym.html')


class FavoritesAnonymView(TemplateView):
    template_name = 'favorites/favorites_for_anonym.html'


def favorite_game_list_ids(request):
    """
    Return list of ids from favorites
    """
    return (
        [game.game_id.game_id for game in UserFavoriteGames.objects.filter(owner=request.user)]
        if request.user.is_authenticated
        else []
    )


def add_to_favorites(request, game_id):
    """
    Add games for favorites
    """
    game = Games.objects.filter(game_id=game_id)[0]
    current_favorite_games = UserFavoriteGames.objects.filter(game_id=game, owner=request.user)
    if not current_favorite_games:
        UserFavoriteGames.objects.create(game_id=game, owner=request.user)
    else:
        current_favorite_games.restore()
    return redirect(request.META.get('HTTP_REFERER'))


def remove_from_favorites(request, game_id):
    """
    Remove games from favorites
    """
    game = Games.objects.filter(game_id=game_id)[0]
    favorite_games = UserFavoriteGames.objects.filter(game_id=game, owner=request.user)
    if favorite_games:
        favorite_games.delete()
    return redirect(request.META.get('HTTP_REFERER'))
