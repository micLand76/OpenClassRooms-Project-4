from datetime import datetime
from operator import itemgetter, attrgetter

from models.menu import Menu
from models.player import Player
from models.tournament import Tournament
from models.round import Round
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
        self.menu.add("auto", "Rapports", ReportMenuController)
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
        self.menu.add("auto", "Associer des Joueurs", AssociatePlayersController)
        self.menu.add("auto", "Consulter", PlayersMenuController)
        self.menu.add("auto", "Saisi des Résultats", EnterResultsController)
        self.menu.add("auto", "Génération des Paires", PairGenerateController)
        self.menu.add("r", "Retour", HomeMenuController)

        user_choice = self.view.get_user_choice("Tournoi")
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
                                self.tournament_view.quest_desc, self.tournament_view.quest_ctrl]
        for quest in questions_tournament:
            good_answer = False
            self.tournament_view.tournament_ask(quest)
            answer = None
            while not good_answer:
                answer = input('>> ')
                if self.is_answer_empty(answer) is True:
                    print('Vous n\'avez rien saisi comme valeur. Veuillez en saisir une.')
                # elif quest == self.tournament_view.quest_nb_round and self.is_numeric(answer) is False:
                    # print('Vous n\'avez pas saisi un entier pour le nombre de rounds.')
                elif quest == self.tournament_view.quest_ctrl and self.is_good_value_time_control(answer) is False:
                    print('Vous ne pouvez saisir qu\'une des trois valeurs suivantes:',
                          'bullet, blitz ou coup rapide.')
                else:
                    good_answer = True
            input_tournament.append(answer)
        self.tournament = Tournament(*input_tournament)
        self.tournament.rounds.append(1)
        self.tournament.insert_tournament(self.tournament.serializ_tournament())
        self.tournament_id = self.tournament.search_id_tournament('name', self.tournament.name)
        return TournamentMenuController

    @staticmethod
    def is_answer_empty(answer: str) -> bool:
        """ check if the user has written something """
        if answer == '':
            return True
        else:
            return False

    @staticmethod
    def is_numeric(answer) -> bool:
        """ check if the answer given is a numeric """
        return answer.isnumeric()

    @staticmethod
    def is_good_value_time_control(answer: str) -> bool:
        """ check if the answer for the time controle type is one of the 3 possibilities
        bullet, blitz or coup rapide """
        time_ctrl = ['blitz', 'bullet', 'coup rapide']
        if answer.lower().strip() not in time_ctrl:
            return False
        return True


class AssociatePlayersController:
    def __init__(self):
        self.player = Player()
        self.tournament = Tournament('', '', '')
        self.tournament_id = 0
        self.player_id = 0

    def __call__(self, tournament_id=0):
        self.tournament_id = tournament_id
        if self.tournament_id == 0:
            print(self.tournament.display_all_table())
            self.tournament_id = input('A quel tournoi voulez-vous associer des joueurs (saisir le n°) ? ')
        print(self.player.display_all_table())

        number_of_players = self.player.number_of_players()
        number_of_player_round = 8
        print("nombre total de joueurs = " + str(number_of_players))

        number_of_players = min(number_of_players, number_of_player_round)
        list_players_selected = []
        i = 0
        while i < number_of_players:
            print('Veuillez saisir le n° du joueur que vous voulez associer pour le tournoi. ')
            self.player_id = int(input())
            """ manage the case of selecting twice the same player """
            if self.player_id in list_players_selected:
                print('Vous avez déjà sélectionné ce joueur')
            else:
                # il faut ajouter les nouveaux players aux anciens, déjà associés
                # auparavant mais pour l'instant on enregistre les 8 joueurs une fois pour toutes
                list_players_selected.append(self.player_id)
                self.update_players_tournament()
                i += 1

        """ continuate: str = input('voulez-vous associer un autre joueur (y/n) ? ')
        if continuate == 'y':
            return self.__call__(self.tournament_id)
        else: """
        return TournamentMenuController

    def update_players_tournament(self):
        self.tournament.players.append(self.player_id)
        self.tournament.update_tournament([int(self.tournament_id)], self.tournament.players)


class EnterResultsController:
    def __init__(self):
        self.player = Player()
        self.tournament = Tournament('', '', '')
        self.round = Round(1, datetime.now())
        self.tournament_id = 0
        self.player_id = 0

    def __call__(self):
        print(self.tournament.display_all_table())
        self.tournament_id = input('Pour quel tournoi voulez-vous générer les paires de joueurs (saisir le n°) ? ')
        list_players_tournament = self.tournament.return_players(int(self.tournament_id))
        self.generate_pairs(list_players_tournament)
        return TournamentMenuController


class PairGenerateController:
    def __init__(self):
        self.player = Player()
        self.tournament = Tournament('', '', '')
        self.round = Round('', '', datetime.now())
        self.tournament_id = 0
        self.player_id = 0

    def __call__(self):
        print(self.tournament.display_all_table())
        self.tournament_id = input('Pour quel tournoi voulez-vous générer les paires de joueurs (saisir le n°) ? ')
        # tester si le tournoi a bien au moins 8 joueurs d'enregistré
        self.round.tournament = self.tournament_id
        self.round.name = self.tournament.return_last_round(self.tournament_id)
        list_players_tournament = self.tournament.return_players(int(self.tournament_id))
        self.generate_pairs(list_players_tournament)
        return TournamentMenuController

    def generate_pairs(self, list_players_tournament: list):
        if self.round.name == 1:
            for i in range(1, len(list_players_tournament), 2):
                players_couple: tuple = (list_players_tournament[i], list_players_tournament[i - 1])
                self.round.pairs.append(players_couple)
        else:
            pass
        print(self.round.pairs)
        self.round.data_hour_start = datetime.now()
        self.round.match = 0
        self.round.result = 0
        self.round.data_hour_end = ''
        self.round.insert_round(self.round.serializ_round())


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
        self.tournament = Tournament("", "", "")

    @staticmethod
    def has_good_format_date(answer_date: str) -> bool:
        """ verify if a date given respect the date format given in the controller.format
        and strftime converts the datetime object containing current
        date and time to the controller.format format """
        try:
            if answer_date != datetime.strptime(answer_date, PlayersCreate.format).strftime(PlayersCreate.format):
                raise ValueError
            return True
        except ValueError:
            return False

    def is_date_question(self, question: str) -> bool:
        """ check if the question is the question that needs an answer with a date """
        return question == self.player_view.quest_birth_date

    @staticmethod
    def is_answer_empty(answer: str) -> bool:
        """ check if the user has written something """
        if answer == '':
            return True
        else:
            return False

    def __call__(self, nb_players=1):
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
            continuate: str = input('Voulez-vous créer un autre joueur (y/n) ? ')
            if continuate == 'y':
                return PlayersCreate
            else:
                return PlayersMenuController


class RankingMenuController:
    pass


class ReportMenuController:
    """ controller of the Report Menu """

    def __init__(self):
        self.menu = Menu()
        self.view = HomeMenuView(self.menu)

    def __call__(self):
        """ we add the entries for the menu of the Report entry """
        self.menu.clear()
        self.menu.add("auto", "Acteurs", ActorsReportController)
        self.menu.add("auto", "Joueurs", PlayersReportController)
        self.menu.add("auto", "Tournois", TournamentsReportController)
        self.menu.add("auto", "Tours", RoundsReportController)
        self.menu.add("auto", "Matchs", MatchsReportController)
        self.menu.add("r", "Retour", HomeMenuController)

        user_choice = self.view.get_user_choice("Rapports")
        """ return of the next controller """
        return user_choice.handler


class ActorsReportController:
    def __init__(self):
        self.player = Player()

    def __call__(self):
        """ displaying the actors according to the sort chosen """
        try:
            sorting_order: int = int(input('Voulez-vous trier les acteurs par ordre alphabétique (1) '
                                           'ou en fonction du rang (2) ? '))
        except:
            sorting_order = 1
        if sorting_order not in (1, 2):
            sorting_order = 1
        print("ID".ljust(4) + ' ' + "Prénom".ljust(15) + ' ' + "Nom".ljust(15) + ' ' + "Date Naiss.".ljust(14) + ' ' +
              "Sexe".ljust(4) + ' ' + "Clas.".ljust(4))
        print(self.player.display_all_table_all_data(sorting_order))

        return ReportMenuController


class PlayersReportController:
    def __init__(self):
        self.player = Player()
        self.tournament = Tournament("", "", "")

    def __call__(self):
        print(self.tournament.display_all_table())
        try:
            id_tournament: int = int(input('Pour quel tournoi voulez-vous afficher les joueurs (saisir le n°) ?'))
            """ displaying the players according to the sort chosen """

        except:
            PlayersReportController()
        try:
            sorting_order: int = int(input('Voulez-vous trier les acteurs par ordre alphabétique (1) '
                                           'ou en fonction du rang (2) ? '))
        except:
            sorting_order = 1
        if sorting_order not in (1, 2):
            sorting_order = 1

        print("Prénom".ljust(15) + ' ' + "Nom".ljust(15) + ' ' + "Date Naiss.".ljust(14) + ' ' +
              "Sexe".ljust(4) + ' ' + "Clas.".ljust(4))
        liste_players: list = self.tournament.return_players(id_tournament)
        print(self.player.display_all_table_all_data_for_tournament(liste_players, sorting_order))
        return ReportMenuController


class TournamentsReportController:
    def __init__(self):
        self.tournament = Tournament("", "", "")

    def __call__(self):
        """ displaying the tournaments """
        print("Nom".ljust(15) + ' ' + "place".ljust(14) + ' ' + "date".ljust(14) + ' ' + "rounds".ljust(14) + ' ' +
              "contrôle du temps".ljust(20) + ' ' + "description".ljust(20))
        print(self.tournament.display_all_tournaments())
        return ReportMenuController


class RoundsReportController:
    pass


class MatchsReportController:
    pass


class ExitMenuController:
    def __call__(self):
        quit()
