from models.tournament import Tournament
from models.player import Player
from views.tournament_view import TournamentView
from views.player_view import PlayerView


class Controller:
    """ Main controller """

    def __init__(self):
        """ we add the tournament view and tournament model to the controller """
        self.tournament = ""
        self.tournament_view = TournamentView()
        self.choices = ""

        self.player = ""
        self.player_view = PlayerView()

    def menu(self):
        self.tournament_question()
        self.player_question()

    def tournament_question(self):
        input_tournament = []
        for quest in (self.tournament_view.quest_name, self.tournament_view.quest_place,
                      self.tournament_view.quest_ctrl, self.tournament_view.quest_desc,
                      self.tournament_view.quest_nb_round):
            self.tournament_view.tournament_ask(quest)
            answer = input('>> ')
            while answer == '':
                print('Vous n\'avez rien saisi comme valeur. Veuillez en saisir une.')
                answer = input('>> ')
            while quest == self.tournament_view.quest_nb_round and answer.isnumeric() is False:
                print('Vous n\'avez pas saisi un entier pour le nombre de rounds.')
                answer = input('>> ')
            input_tournament.append(answer)
        self.tournament = Tournament(*input_tournament)
        self.tournament.insert_tournament()
        # self.tournament.insert_tournament('test', 'paris', 'tournoi de test')

    def update_tournament(self):
        self.tournament = Tournament(*self.choices)

    def player_question(self):
        input_player = []
        for quest in (self.player_view.quest_name, self.player_view.quest_last_name,
                      self.player_view.quest_birth_date, self.player_view.quest_sex):
            self.player_view.player_ask(quest)
            answer = input('>> ')
            while answer == '':
                print('Vous n\'avez rien saisi comme valeur. Veuillez en saisir une.')
                answer = input('>> ')
            while quest == self.player_view.quest_birth_date and answer.isnumeric() is False:
                print('Vous n\'avez pas saisi une date pour la date de naissance.')
                answer = input('>> ')
            input_player.append(answer)
        self.player = Player(*input_player)
        self.player.insert_player()
