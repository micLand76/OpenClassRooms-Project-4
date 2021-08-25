

from controllers.menu_management import HomeMenuController
from models.tournament import Tournament
from models.player import Player
from views.tournament_view import TournamentView
from views.player_view import PlayerView


class Controller:
    """ Main controller """
    def __init__(self):
        self.controller = None

    def start(self):
        self.controller = HomeMenuController()
        while self.controller:
            self.controller = self.controller()
