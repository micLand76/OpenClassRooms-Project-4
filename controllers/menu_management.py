from datetime import datetime

from models.menu import Menu
from models.player import Player
from models.tournament import Tournament
from views.menu_view import HomeMenuView
from views.player_view import PlayerView
from views.tournament_view import TournamentView


class HomeMenuController:
    """ Controller of the Beginning Menu """
    def __init__(self):
        self.menu = Menu()
        self.view = HomeMenuView(self.menu)

    def __call__(self):
        """ we add the entries for the menus at the beginning of the app
        we let the prog to give the number of the menu (auto) """
        self.menu.clear()
        self.menu.add("auto", "Tournois", TournamentMenuController)
        self.menu.add("auto", "Joueurs", PlayersMenuController)
        self.menu.add("auto", "Classement", RankingMenuController)
        self.menu.add("q", "Quitter", ExitMenuController)

        user_choice = self.view.get_user_choice("Accueil")
        """ return of the next controller """
        return user_choice.handler


class TournamentMenuController:
    """ controller of the Tournament Menu """
    def __init__(self):
        self.menu = Menu()
        self.view = HomeMenuView(self.menu)

    def __call__(self):
        """ we add the entries for the menu of the Tournament entry """
        self.menu.clear()
        self.menu.add("auto", "Créer", TournamentCreate)
        self.menu.add("auto", "Consulter", PlayersMenuController)
        self.menu.add("auto", "Modifier", RankingMenuController)
        self.menu.add("r", "Retour", HomeMenuController)

        user_choice = self.view.get_user_choice("Tournament")
        """ return of the next controller """
        return user_choice.handler


class TournamentCreate:
    def __init__(self):
        """ we add the tournament view and tournament model to the controller """
        self.tournament = Tournament("", "", "")
        self.tournament_view = TournamentView()
        self.tournament_id = None

    def __call__(self):
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
                if self.is_answer_empty(answer) is True:
                    print('Vous n\'avez rien saisi comme valeur. Veuillez en saisir une.')
                elif self.is_numeric_question(quest) is True and self.is_numeric(answer) is False:
                    print('Vous n\'avez pas saisi un entier pour le nombre de rounds.')
                elif self.is_value_control(quest, answer) is False:
                    print('Vous ne pouvez saisir qu\'une des trois valeurs suivantes:',
                          'bullet, blitz ou coup rapide.')
                else:
                    good_answer = True
            input_tournament.append(answer)
        self.tournament = Tournament(*input_tournament)
        self.tournament.insert_tournament(self.tournament.serializ_tournament())
        self.tournament_id = self.tournament.search_id_tournament('name', self.tournament.name)

    @staticmethod
    def is_answer_empty(answer: str) -> bool:
        """ check if the user has written something """
        if answer == '':
            return True

    @staticmethod
    def is_numeric(answer) -> bool:
        """ check if the answer given is a numeric """
        return answer.isnumeric()

    def is_numeric_question(self, question) -> bool:
        """ check if the question is the question that needs an answer with a numeric """
        return question == self.tournament_view.quest_nb_round

    def is_value_control(self, question, answer) -> bool:
        """ check if the answer for the time controle type is one of the 3 possibilities
        bullet, blitz or coup rapide """
        time_ctrl = ['blitz', 'bullet', 'coup rapide']
        if question == self.tournament_view.quest_ctrl and answer.lower().strip() not in time_ctrl:
            return False
        return True


class RankingMenuController:
    pass


class PlayersMenuController:
    def __init__(self):
        self.menu = Menu()
        self.view = HomeMenuView(self.menu)

    def __call__(self):
        self.menu.clear()
        self.menu.add("auto", "Créer", PlayersCreate)
        self.menu.add("auto", "Consulter", PlayersMenuController)
        self.menu.add("auto", "Modifier", RankingMenuController)
        self.menu.add("r", "Retour", HomeMenuController)

        user_choice = self.view.get_user_choice("Players")
        """ return of the next controller """
        return user_choice.handler


class PlayersCreate:

    format = "%d/%m/%Y"

    def __init__(self):
        """ we add the player view and player model to the controller """
        self.player = Player()
        self.player_view = PlayerView()
        self.player_id = None
        self.tournament = Tournament()

    @staticmethod
    def has_good_format_date(answer_date) -> bool:
        """ verify if a date given respect the date format given in the controller.format
        and strftime converts the datetime object containing current
        date and time to the controller.format format """
        try:
            if answer_date != datetime.strptime(answer_date, PlayersCreate.format).strftime(PlayersCreate.format):
                raise ValueError
            return True
        except ValueError as err:
            return False

    def is_date_question(self, question) -> bool:
        """ check if the question is the question that needs an answer with a date """
        return question == self.player_view.quest_birth_date

    @staticmethod
    def is_answer_empty(answer: str) -> bool:
        """ check if the user has written something """
        if answer == '':
            return True

    def update_players_tournament(self, player):
        self.tournament.update_tournament(self.tournament.tournament_id, 'players', player)

    def __call__(self, nb_players=8):
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
                    if self.is_answer_empty(answer) is True:
                        """ test the answer is not empty """
                        print('Vous n\'avez rien saisi comme valeur. Veuillez en saisir une.')
                    elif self.is_date_question(quest) and self.has_good_format_date(answer) is False:
                        """ verify the date format """
                        print('Vous n\'avez pas saisi le bon format pour la date de naissance (dd/mm/yyyy).')
                    else:
                        good_answer = True
                input_player.append(answer)
            self.player = Player(*input_player)
            self.player.insert_player(self.player.serializ_player())
            self.player_id = self.player.search_id_player('name', self.player.name)
            self.update_players_tournament(self.player_id)


class ExitMenuController:
    def __call__(self):
        quit()
