from datetime import datetime
from operator import itemgetter, attrgetter

from models.match import Match
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
        self.menu.add("auto", "Génération des Paires", PairGenerateController)
        self.menu.add("auto", "Saisi des Résultats", EnterResultsController)
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
            self.tournament_id = int(input('Pour quel tournoi voulez-vous associer des joueurs (saisir le n°) ? '))
            if self.tournament.return_nb_players_per_tournament(self.tournament_id) == 8:
                change_selection = input('Vous avez déjà sélectionné 8 joueurs pour ce tournoi. '
                                         'Voulez-vous changer cette sélection (y/n) ?')
                if change_selection == 'n':
                    return TournamentMenuController

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
        return TournamentMenuController

    def update_players_tournament(self):
        self.tournament.players.append(self.player_id)
        self.tournament.update_tournament([int(self.tournament_id)], self.tournament.players)


class EnterResultsController:
    def __init__(self):
        self.player = Player()
        self.tournament = Tournament('', '', '')
        self.round = Round('', '', datetime.now())
        self.match = Match(0, 0, 0, 0, 0, 0)
        self.tournament_id = 0
        self.player_id = 0
        self.round_name = 0
        self.round_id = 0
        self.match_id = 0

    def __call__(self):
        list_tournaments = self.tournament.display_all_table_with_players()
        # AJOUTER UN TEST POUR VERIFIER S'IL Y A DEJA EU LA PAIRISATION
        if list_tournaments == '':
            print('Vous n\'avez associé 8 joueurs à aucun tournoi')
        else:
            print(list_tournaments)
            self.tournament_id = int(input('Pour quel tournoi voulez-vous générer les paires de joueurs (saisir le '
                                           'n°) ? \n '))
            self.round_name = self.tournament.return_rounds(self.tournament_id)[-1]
            self.round_id = self.round.search_id_round('tournament', self.tournament_id)
            list_players: list = self.round.return_old_pairs(self.round_id)
            if len(list_players) == 4:
                print(list_players)
                player_score = int(input("Pour quel paire de joueurs voulez-vous saisir les points (1, 2, 3 ou 4) ? \n"))
                match_already = self.match.search_match('id_tournament', self.tournament_id)
                for m_already in match_already:
                    if (m_already['player_1'], m_already['player_2']) == \
                            (list_players[player_score-1][0], list_players[player_score-1][1]) and \
                            m_already['round_name'] == self.round_name:
                        print('Vous avez déjà indiqué le gagnant de ce match')
                        return TournamentMenuController
                winner = int(input("Qui est le gagant du match (n° du joueur ou 0 si match nul) ? \n "))
                self.match.id_tournament = self.tournament_id
                self.match.round_name = self.round_name
                self.match.player_1 = list_players[player_score-1][0]
                self.match.player_2 = list_players[player_score-1][1]
                self.match.attribut_points(winner)
                self.match.insert_match()
                round_matchs = self.match.search_id_match('id_tournament', self.match.id_tournament)
                list_matchs: list = self.round.return_matchs_id(self.round_id)
                list_matchs.append(round_matchs)
                self.round.update_round(self.round_id, 'match_id', list_matchs)
                """ if all the 4 matchs has been played, we can close the round """
                if len(list_matchs) == 4:
                    self.round.update_round(self.round_id, 'data_hour_end', datetime.now())
            else:
                print("Vous ne pouvez pas saisir de score pour ce tournoi car il n'y a pas assez de paires de"
                      " joueurs pour son dernier round ")
        return TournamentMenuController


class PairGenerateController:
    def __init__(self):
        self.player = Player()
        self.tournament = Tournament('', '', '')
        self.round = Round('', '', datetime.now())
        self.tournament_id = 0
        self.player_id = 0
        self.round_id = 0

    def __call__(self):
        list_tournaments = self.tournament.display_all_table_with_players()
        if list_tournaments == '':
            print('Vous n\'avez associé 8 joueurs à aucun tournoi')
        else:
            print(list_tournaments)
            self.tournament_id = int(
                input('Pour quel tournoi voulez-vous générer les paires de joueurs (saisir le n°) ? '))
            """ confirm that the last round is finish before created a new one """
            self.round.tournament = self.tournament_id
            self.round.name = self.tournament.return_rounds(self.tournament_id)[-1]
            self.round_id = self.round.search_id_round('tournament', self.tournament_id)
            if self.round.round_closed(self.round_id) is True:
                list_players_tournament = self.tournament.return_players(self.tournament_id)
                list_player = []
                for player in list_players_tournament:
                    list_player.append(self.player.return_player_ranking(player))
                self.tournament.rounds = self.tournament.return_rounds(self.tournament_id)
                self.tournament.rounds.append(int(self.round.name) + 1)
                self.tournament.update_tournament_round(self.tournament_id, self.tournament.rounds)
                self.generate_pairs(list_players_tournament, list_player)
            else:
                print("Vous n'avez pas saisi tous les résultats des matchs pour le round en cours, vous ne pouvez pas "
                      "en créer un nouveau.")
        return TournamentMenuController

    def generate_pairs(self, list_players_tournament: list, list_player: list):
        if self.round.name == 1:
            for i in range(1, len(list_players_tournament), 2):
                players_couple: tuple = (list_players_tournament[i], list_players_tournament[i - 1])
                self.round.pairs.append(players_couple)
        else:
            old_list_players: list = self.round.return_old_pairs(self.round_id)
            print('old_list_players', old_list_players)
            self.round.pairs.extend(self.round.generate_pair(list_player, old_list_players))
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
                self.player_view.player_ask(quest)
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
