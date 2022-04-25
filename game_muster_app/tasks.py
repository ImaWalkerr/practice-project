from __future__ import absolute_import, unicode_literals
from celery import shared_task, Celery

from game_muster_app.managers.game_manager import GAME_MANAGER


app = Celery('game_muster', broker='redis://127.0.0.1:6379/0')


@shared_task
def refresh_games():
    """
    Celery task - Refresh games by generating new ones by games manager
    """
    refresh_games_start = GAME_MANAGER.create_game_from_igdb()
