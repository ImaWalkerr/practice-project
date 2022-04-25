from django.core.management.base import BaseCommand
from game_muster_app.managers.game_manager import GAME_MANAGER


class Command(BaseCommand):
    """
    Start base_game_manager script for download games in database
    """
    def handle(self, *args, **options):
        games = GAME_MANAGER.create_game_from_igdb()
        return "Script successfully complete"
