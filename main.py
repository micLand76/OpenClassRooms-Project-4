from pprint import pprint
import views.matchview
from models.player import Player
from models.tournament import Tournament
from controllers.base import Controller
from views.tournament_view import TournamentView

if __name__ == "__main__":
    ''' appel au controler pour:
        créer les joueurs
        créer un tournoi
        créer le 1er round avec génération des paires
        génération du match
        entrée des résultats
        entrée du classement
        maj round
        génération 2e round

    '''
    #tournament = Tournament('Tournoi 1', 'Paris', '30/07/21', 'Tournoi ete')
    #tournament_view = TournamentView()
    controller = Controller()
    controller.menu()

    """
    pt = Player()
    pt.insert_player('Martin', 'John', '19/09/1976', 'M', 5)
    id_player = pt.search_player('name', 'Martin')
    print("id_player :", id_player)
    print(pt.search_player_by_id(12))
    print('le joueur est: ', pt.search_player('name', views.matchview.search_player_by_name()))"""
    # print(len(pt.player))
    # pt.update_player()
    # MatchView()
