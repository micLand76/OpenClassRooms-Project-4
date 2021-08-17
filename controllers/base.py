from datetime import datetime

from models.tournament import Tournament
from models.player import Player
from views.tournament_view import TournamentView
from views.player_view import PlayerView


def validate(date_text):
    """ verify if a date given respect the date format given in the controller.format
    and strftime converts the datetime object containing current
    date and time to the controller.format format """
    return date_text != datetime.strptime(
        date_text, Controller.format
    ).strftime(Controller.format)


class Controller:
    """ Main controller """

    format = "%d/%m/%Y"

    def __init__(self):
        """ we add the tournament view and tournament model to the controller """
        self.tournament = None
        self.tournament_view = TournamentView()
        self.tournament_id = None

        self.player = ""
        self.player_view = PlayerView()

    def menu(self):
        self.tournament_question()
        self.player_question(3)

    def tournament_question(self):
        """ we ask the questions about the tournament and we add them to the instance of tournament
        and insert them into the Tinydb table Tournament """
        input_tournament = []
        questions_tournament = [self.tournament_view.quest_name, self.tournament_view.quest_place,
                                self.tournament_view.quest_ctrl, self.tournament_view.quest_desc,
                                self.tournament_view.quest_nb_round]
        for quest in questions_tournament:
            good_answer = False
            self.tournament_view.tournament_ask(quest)
            answer = None
            while not good_answer:
                answer = input('>> ')
                if answer == '':
                    print('Vous n\'avez rien saisi comme valeur. Veuillez en saisir une.')
                elif quest == self.tournament_view.quest_nb_round and answer.isnumeric() is False:
                    print('Vous n\'avez pas saisi un entier pour le nombre de rounds.')
                else:
                    good_answer = True
            input_tournament.append(answer)
        self.tournament = Tournament(*input_tournament)
        self.tournament.insert_tournament(self.tournament.serializ_tournament())
        self.tournament_id = self.tournament.search_id_tournament('name', self.tournament.name)

    @staticmethod
    def verif_answer_empty(answer):
        if answer == '':
            print('Vous n\'avez rien saisi comme valeur. Veuillez en saisir une.')
            return True

    @staticmethod
    def verif_format_date(answer_date):
        if validate(answer_date) is False:
            print('Vous n\'avez pas saisi le bon format pour la date de naissance (dd/mm/yyyy).')
            return True

    def update_players_tournament(self, player):
        self.tournament.update_tournament(self.tournament_id, 'players', player)

    def player_question(self, nb_players=8):
        """ we ask the questions about the players and we add them to the instance of players
        and insert them into the Tinydb table Player
         we loop those questions for all the players we want to add """
        for player in range(1, nb_players + 1):
            input_player = []
            questions_player = [self.player_view.quest_name, self.player_view.quest_last_name,
                                self.player_view.quest_birth_date, self.player_view.quest_sex]
            for quest in questions_player:
                good_answer = False
                self.player_view.player_ask(quest, player)
                answer = None
                while not good_answer:
                    answer = input('>> ')
                    if self.verif_answer_empty(answer) is True:
                        """ test the answer is not empty """
                        # print('Vous n\'avez rien saisi comme valeur. Veuillez en saisir une.')
                    elif quest == self.player_view.quest_birth_date and self.verif_format_date(answer) is True:
                        """ verify the date format """
                        # print('Vous n\'avez pas saisi le bon format pour la date de naissance (dd/mm/yyyy).')
                    else:
                        good_answer = True
                input_player.append(answer)
            self.player = Player(*input_player)
            self.player.insert_player(self.player.serializ_player())
            self.update_players_tournament(self.player.serializ_player())
