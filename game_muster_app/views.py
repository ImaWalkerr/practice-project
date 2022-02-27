import requests
from django import views
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.views.generic import ListView, CreateView

from .models import Profile
from .forms import LoginForm, RegistrationForm

from game_muster_app.api.igdb_wrapper import IGDB_WRAPPER


class MainPageView(views.View):
    """
    Список всех игр на главной странице
    """

    def get(self, request):

        try:
            games = IGDB_WRAPPER.get_games()
            if not games:
                raise LookupError
        except LookupError:
            return HttpResponseNotFound(f"<h1>There are no games found!</h1>")

        pagination = Paginator(games, 6)
        page_number = request.GET.get('page')
        page_obj = pagination.get_page(page_number)
        nums = "a" * page_obj.paginator.num_pages

        all_platforms_filter = IGDB_WRAPPER.get_platforms()
        all_genres_filter = IGDB_WRAPPER.get_genres()

        users = Profile.objects.all()

        context = {
            'games': games,
            'page_obj': page_obj,
            'nums': nums,
            'all_platforms_filter': all_platforms_filter,
            'all_genres_filter': all_genres_filter,
            'users': users
        }

        return render(request, 'main_page.html', context)


class GamesDetailPageView(views.View):
    """
    Информация по конкретной игре
    """

    def get(self, request, game_id):
        target_game = IGDB_WRAPPER.get_game(game_id)
        target_game = target_game[0] if target_game else None
        genres = target_game.get('genres')
        platforms = target_game.get('platforms')
        release_dates = target_game.get('release_dates')
        rating = target_game.get('rating')
        total_rating = target_game.get('total_rating')
        aggregated_rating = target_game.get('aggregated_rating')
        aggregated_rating_count = target_game.get('aggregated_rating_count')
        cover = target_game.get('cover')
        screenshots = target_game.get('screenshots')

        context = {
            'target_game': target_game,
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
            Profile.objects.create(
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


class ProfileView(views.View):

    def get(self, request):
        user_info = Profile.objects.all()
        context = {
            'user_info': user_info
        }
        return render(request, 'profile_page.html', context)
