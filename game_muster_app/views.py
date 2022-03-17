from django import views
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.http import urlsafe_base64_decode
from django.views.generic.base import TemplateView
from math import ceil

from .models import *
from .forms import LoginForm, RegistrationForm
from game_muster_app.api.igdb_wrapper import IGDB_WRAPPER
from .utils import send_email_for_verify


class BasePageView(TemplateView):

    template_name = 'base.html'

    def get(self, *args, **kwargs):

        users = GameUser.objects.all()

        context = {
            'users': users
        }

        return context


class MainPageView(views.View):
    """
    Functional for main page
    """
    def get(self, request):

        igdb_search = request.GET.get('search_game')
        platforms = request.GET.getlist('platform_id')
        genres = request.GET.getlist('genre_id')
        ratings_min = int(request.GET.get('min') or 0)
        ratings_max = int(request.GET.get('max') or 100)
        ratings = ratings_min, ratings_max
        page_number = request.GET.get('page') or 1

        try:
            games = IGDB_WRAPPER.get_games_by_filtering(
                search=igdb_search, platforms=platforms, genres=genres, ratings=ratings, page=int(page_number)
            )
            if not games:
                raise LookupError
        except LookupError:
            return render(request, 'search_error.html')

        count = IGDB_WRAPPER.get_games_count(
            search=igdb_search, platforms=platforms, genres=genres, ratings=ratings
        )
        games_count = ceil(count / 6)

        all_platforms_filter = IGDB_WRAPPER.get_platforms()
        all_genres_filter = IGDB_WRAPPER.get_genres()

        context = {
            'games': games,
            'games_count': range(games_count),
            'all_platforms_filter': all_platforms_filter,
            'all_genres_filter': all_genres_filter,
        }

        return render(request, 'main_page.html', context)


class ErrorSearchView(TemplateView):
    template_name = 'error_search.html'


class GamesDetailPageView(views.View):
    """
    Functional for current game page
    """
    def get(self, request, game_id):
        current_game = IGDB_WRAPPER.get_game_id(game_id)
        current_game = current_game[0] if current_game else None
        genres = current_game.get('genres')
        platforms = current_game.get('platforms')
        release_dates = current_game.get('release_dates')
        rating = current_game.get('rating')
        total_rating = current_game.get('total_rating')
        aggregated_rating = current_game.get('aggregated_rating')
        aggregated_rating_count = current_game.get('aggregated_rating_count')
        cover = current_game.get('cover')
        screenshots = current_game.get('screenshots')

        context = {
            'current_game': current_game,
            'genres': genres,
            'platforms': platforms,
            'release_dates': release_dates,
            'rating': rating,
            'total_rating': total_rating,
            'aggregated_rating': aggregated_rating,
            'aggregated_rating_count': aggregated_rating_count,
            'cover': cover,
            'screenshots': screenshots,
        }
        return render(request, 'games_detail_page.html', context)


class ProfileView(views.View):

    def get(self, request):
        users = GameUser.objects.filter(user=request.user)
        context = {
            'users': users
        }

        return render(request, 'registration/profile_page.html', context)


class LoginView(views.View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'registration/log_in_page.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
        context = {
            'form': form
        }
        return render(request, 'registration/log_in_page.html', context)


class RegistrationView(views.View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'registration/sign_up_page.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            GameUser.objects.create(
                user=new_user,
                birthday=form.cleaned_data['birthday'],
                gender=form.cleaned_data['gender'],
                age=form.cleaned_data['age']
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            send_email_for_verify(request, user)
            return redirect('confirm_email')
        context = {
            'form': form
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
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user


class InvalidVerifyView(TemplateView):
    template_name = 'registration/invalid_verify.html'


class ConfirmEmailView(TemplateView):
    template_name = 'registration/confirm_email.html'


def do_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponse(f'You must login first!')
