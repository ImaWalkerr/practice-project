from __future__ import absolute_import, unicode_literals
from celery import shared_task

from game_muster_app.managers.base_game_manager import GamesManager
from game_muster_app.models import Games


@shared_task
def refresh_games():
    """
    Celery task - Refresh games by generating new ones by games manager
    """
    latest_game = (
        Games.objects.exclude(release_dates=None).order_by('-release_dates').first()
    )
    last_release_date = latest_game.release_dates if latest_game else None

    GamesManager.generate_list_of_games(last_release_date)
