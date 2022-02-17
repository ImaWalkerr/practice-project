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

    # дикт с ключем в виде id картинки, а значение - ссыка на картинку из igdb wrapper

    genres = target_game['genres']
    platforms = target_game['platforms']
    cover = target_game['cover']
    screenshots = target_game['screenshots']

    context = {
        'target_game': target_game,
        'genres': genres,
        'platforms': platforms,
        'cover': cover,
        'screenshots': screenshots,
    }
    return render(request, 'games_detail_page.html', context)

