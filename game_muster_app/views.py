import requests
from django import views
from django.db.models import Q
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.views.generic import ListView

from django.db import models

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

        context = {
            'games': games,
            'page_obj': page_obj,
            'nums': nums,
            'all_platforms_filter': all_platforms_filter,
            'all_genres_filter': all_genres_filter
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
