import requests
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views.generic import ListView


from django.db import models

from game_muster_app.api.igdb_wrapper import IGDB_WRAPPER


def main_page(request):

    games = IGDB_WRAPPER.get_games()
    context = {
        'games': games
    }
    return render(request, 'main_page.html', context)


def games_detail_page(request, game_id):

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

