from django import views
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.views.generic.base import TemplateView
from django.views.decorators.cache import cache_page
from math import ceil
import json

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


@method_decorator(cache_page(60*60), name='get')
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

        # for item in games:
            # if 'cover' in item.keys():
                # item['url'] = item['cover']['url'].replace('t_thumb', 't_cover_big')
            # return games

        context = {
            'games': games,
            'games_count': range(games_count),
            'all_platforms_filter': all_platforms_filter,
            'all_genres_filter': all_genres_filter,
            'title': 'GameMuster',
        }

        return render(request, 'main_page.html', context)


class ErrorSearchView(TemplateView):
    template_name = 'error_search.html'


@method_decorator(cache_page(60*60), name='get')
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
        if cover is not None:
            cover['url'] = cover['url'].replace('t_thumb', 't_cover_big')
        else:
            cover = current_game.get('cover')
        screenshots = current_game.get('screenshots')

        # for item in screenshots:
            # if 'url' in item.keys():
                # item['url'] = item['url'].replace('t_thumb', 't_screenshot_huge')
            # return screenshots

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
            'title': 'Game details',
        }
        return render(request, 'games_detail_page.html', context)


class ProfileView(views.View):

    def get(self, request):
        users = GameUser.objects.filter(user=request.user)
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
        return redirect('logout_done')
    else:
        return HttpResponse(f'You must login first!')


class LogoutDoneView(TemplateView):
    template_name = 'registration/logout_done.html'


@method_decorator(cache_page(60*60), name='get')
class MyFavoritesView(views.View):

    def get(self, request):
        favorites_list = request.session.get('favorites')
        paginator = Paginator(favorites_list, 12)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        num_of_pages = "a" * page_obj.paginator.num_pages

        context = {
            'favorites_list': favorites_list,
            'page_obj': page_obj,
            'num_of_pages': num_of_pages,
            'title': 'My favorites',
        }
        return render(request, 'favorites/favorites_page.html', context)


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def add_to_favorites(request):
    if request.method == 'POST':
        if not request.session.get('favorites'):
            request.session['favorites'] = list()
        else:
            request.session['favorites'] = list(request.session['favorites'])

        item_exist = next(
            (item for item in request.session['favorites']
             if item["type"] == request.POST.get('type')
             and item["id"] == request.POST.get('id')
             and item["genres"] == request.POST.get('genres')
             and item["url_root"] == request.POST.get('url_root')), False
        )
        add_data = {
            'type': request.POST.get('type'),
            'id': request.POST.get('id'),
            'genres': request.POST.get('genres'),
            'url_root': request.POST.get('url_root'),
        }

        if not item_exist:
            request.session['favorites'].append(add_data)
            request.session.modified = True

    if is_ajax(request=request):
        data = {
            'type': request.POST.get('type'),
            'id': request.POST.get('id'),
            'genres': request.POST.get('genres'),
            'url_root': request.POST.get('url_root'),
        }
        request.session.modified = True
        return JsonResponse(data)
    return redirect(request.POST.get('url_from'))


def remove_from_favorites(request):
    if request.method == 'POST':

        for item in request.session['favorites']:
            if item['id'] == request.POST.get('id') \
                    and item['type'] == request.POST.get('type') \
                    and item['genres'] == request.POST.get('genres') \
                    and item['url_root'] == request.POST.get('url_root'):
                item.clear()

        while {} in request.session['favorites']:
            request.session['favorites'].remove({})

        if not request.session['favorites']:
            del request.session['favorites']

        request.session.modified = True

        if is_ajax(request=request):
            data = {
                'type': request.POST.get('type'),
                'id': request.POST.get('id'),
                'genres': request.POST.get('genres'),
                'url_root': request.POST.get('url_root'),
            }
            request.session.modified = True
            return JsonResponse(data)
        return redirect(request.POST.get('url_from'))


def delete_favorites(request):
    if request.session.get('favorites'):
        del request.session['favorites']
        request.session.modified = True
    return redirect('/')


def favorites_api(request):
    return JsonResponse(request.session.get('favorites'), safe=False)
