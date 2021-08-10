from datetime import datetime

from models.tournament import Tournament
from models.player import Player
from views.tournament_view import TournamentView
from views.player_view import PlayerView


def validate(date_text):
    try:
        if date_text != datetime.strptime(date_text, Controller.format).strftime(Controller.format):
            raise ValueError
        return True
    except ValueError:
        return False


class Controller:
    """ Main controller """

    format = "%d/%m/%Y"

    def __init__(self):
        """ we add the tournament view and tournament model to the controller """
        self.tournament = ""
        self.tournament_view = TournamentView()
        self.choices = ""

        self.player = ""
        self.player_view = PlayerView()

    def menu(self):
        self.tournament_question()
        self.player_question(3)

    def tournament_question(self):
        input_tournament = []
        questions_tournament = [self.tournament_view.quest_name, self.tournament_view.quest_place,
                                self.tournament_view.quest_ctrl, self.tournament_view.quest_desc,
                                self.tournament_view.quest_nb_round]
        for quest in questions_tournament:
            good_answer = False
            self.tournament_view.tournament_ask(quest)
            answer = None
            while not good_answer:
                good_answer = True
                answer = input('>> ')
                if answer == '':
                    print('Vous n\'avez rien saisi comme valeur. Veuillez en saisir une.')
                    good_answer = False
                elif quest == self.tournament_view.quest_nb_round and answer.isnumeric() is False:
                    print('Vous n\'avez pas saisi un entier pour le nombre de rounds.')
                    good_answer = False
            input_tournament.append(answer)
        self.tournament = Tournament(*input_tournament)
        self.tournament.insert_tournament(self.tournament.serializ_tournament())

    def update_tournament(self):
        self.tournament = Tournament(*self.choices)

    def update_players_tournament(self, player):
        self.tournament.players.append(player)

    def player_question(self, nb_players=8):
        for player in range(1, nb_players+1):
            input_player = []
            questions_player = [self.player_view.quest_name, self.player_view.quest_last_name,
                                self.player_view.quest_birth_date, self.player_view.quest_sex]
            for quest in questions_player:
                good_answer = False
                self.player_view.player_ask(quest, player)
                answer = None
                while not good_answer:
                    good_answer = True
                    answer = input('>> ')
                    if answer == '':
                        print('Vous n\'avez rien saisi comme valeur. Veuillez en saisir une.')
                        good_answer = False
                    elif quest == self.player_view.quest_birth_date and \
                            validate(answer) is False:
                        print('Vous n\'avez pas saisi le bon format pour la date de naissance (dd/mm/yyyy).')
                        good_answer = False
                input_player.append(answer)
            self.player = Player(*input_player)
            self.player.insert_player(self.player.serializ_player())

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
