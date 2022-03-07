from django import views
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator

from .models import *
from .forms import LoginForm, RegistrationForm

from game_muster_app.api.igdb_wrapper import IGDB_WRAPPER


class MainPageView(views.View):
    """
    Functional for main page
    """
    def get(self, request):

        igdb_search = request.GET.get('search_game')
        platforms = request.GET.get('platform_id')
        genres = request.GET.get('genre_id')
        ratings_min = request.GET.get('min')
        ratings_max = request.GET.get('max')
        ratings = ratings_min, ratings_max
        games = IGDB_WRAPPER.get_base_page_games()

        if igdb_search and platforms and genres and ratings is None:
            games = IGDB_WRAPPER.get_base_page_games()
        elif igdb_search is not None:
            games = IGDB_WRAPPER.get_games_by_search(search=igdb_search)
        elif platforms and genres and ratings is not None:
            games = IGDB_WRAPPER.get_games_by_filtering(platforms=platforms, genres=genres, ratings=ratings)
        elif platforms is None and genres and ratings is not None:
            games = IGDB_WRAPPER.get_games_by_filtering(genres=genres, ratings=ratings)
        elif platforms and ratings is not None and genres is None:
            games = IGDB_WRAPPER.get_games_by_filtering(platforms=platforms, ratings=ratings)

        pagination = Paginator(games, 6)
        page_number = request.GET.get('page')
        page_obj = pagination.get_page(page_number)
        nums = "a" * page_obj.paginator.num_pages

        all_platforms_filter = IGDB_WRAPPER.get_platforms()
        all_genres_filter = IGDB_WRAPPER.get_genres()

        users = GameUser.objects.all()

        context = {
            'games': games,
            'page_obj': page_obj,
            'nums': nums,
            'all_platforms_filter': all_platforms_filter,
            'all_genres_filter': all_genres_filter,
            'users': users,
            'platforms': platforms,
            'genres': genres,
        }

        return render(request, 'main_page.html', context)


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


class LoginView(views.View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'log_in_page.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'log_in_page.html', context)


class RegistrationView(views.View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'sign_up_page.html', context)

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
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'sign_up_page.html', context)


def do_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponse(f'You must login first!')
