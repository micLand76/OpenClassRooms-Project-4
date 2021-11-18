from datetime import datetime

from models.match import Match
from models.menu import Menu
from models.player import Player
from models.tournament import Tournament
from models.round import Round
from views.menu_view import HomeMenuView
from views.player_view import PlayerView
from views.tournament_view import TournamentView

""" it's the main file, where there's all the controllers
 the HomeMenuController is called at the beginning of the app """


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

    def __call__(self) -> str:
        """ we add the entries for the menu of the Tournament entry """
        self.menu.clear()
        self.menu.add("auto", "Créer", TournamentCreate)
        self.menu.add("auto", "Associer des Joueurs", AssociatePlayersController)
        self.menu.add("auto", "Génération des Paires", PairGenerateController)
        self.menu.add("auto", "Saisi des Résultats", EnterResultsController)
        self.menu.add("r", "Retour", HomeMenuController)

        user_choice = self.view.get_user_choice("Tournoi")
        """ return of the next controller """
        return user_choice.handler


class TournamentCreate:
    """ creation of a tournament based on some questions: name of the tournament, place
    description and type of tournament (bullet, blitz or coup rapide) """

    def __init__(self):
        """ we add the tournament view and tournament model to the controller """
        self.tournament = Tournament(None, None, None)
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
        """ once the tournament is created, we instantiate a round """
        self.tournament.rounds.append(0)
        """ the round is associated with the tournament """
        self.tournament.insert_tournament(self.tournament.serializ_tournament())
        self.tournament_id = self.tournament.search_id_tournament('name', self.tournament.name)
        return TournamentMenuController

    @staticmethod
    def is_answer_empty(answer: str) -> bool:
        """ check if the user has written something """
        if answer == "":
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
    """ it's the first step after a creation of a new tournament: associate to it 8 players """

    def __init__(self):
        self.player = Player()
        self.tournament = Tournament(None, None, None)
        self.tournament_id = 0
        self.player_id = 0

    def __call__(self, tournament_id: int = 0):
        """ to associate 8 players (number of players for a tournament) to a tournament,
        we first need to choice a tournament, be sure that there's no players already associated,
        after that, we can choose 8 players in the list of all the players """
        self.tournament_id = tournament_id
        if self.tournament_id == 0:
            print(self.tournament.display_all_table())
            self.tournament_id = int(input('Pour quel tournoi voulez-vous associer des joueurs (saisir le n°) ? '))
            if self.tournament.return_nb_players_per_tournament(self.tournament_id) == 8:
                change_selection: str = input('Vous avez déjà sélectionné 8 joueurs pour ce tournoi. '
                                              'Voulez-vous changer cette sélection (y/n) ?')
                if change_selection == 'n':
                    return TournamentMenuController
        print(self.player.display_all_table())
        number_of_players: int = self.player.number_of_players()
        number_of_player_round: int = 8
        print("nombre total de joueurs = " + str(number_of_players))
        number_of_players = min(number_of_players, number_of_player_round)
        list_players_selected: list = []
        i: int = 0
        while i < number_of_players:
            print('Veuillez saisir le n° du joueur que vous voulez associer pour le tournoi. ')
            self.player_id = int(input())
            """ manage the case of selecting a number of player who doesn't exist """
            if self.player.player_exists(self.player_id) is False:
                print('Ce joueur n\'existe pas')
            elif self.player_id in list_players_selected:
                """ manage the case of selecting twice the same player"""
                print('Vous avez déjà sélectionné ce joueur')
            else:
                list_players_selected.append(self.player_id)
                self.update_players_tournament()
                i += 1
        return TournamentMenuController

    def update_players_tournament(self):
        """ once you've selected the players, you can insert them into the database
        first we add them to the player attribut of tournament instance
        and we can call the update_tournament method to update the database """
        self.tournament.players.append(self.player_id)
        self.tournament.update_tournament([int(self.tournament_id)])


class PairGenerateController:
    """ method to generate the pairs of players based on the swiss algorithm
     we need to be sure that the last round is closed before generate new pairs """

    def __init__(self):
        self.player = Player()
        self.tournament = Tournament(None, None, None)
        self.round = Round(None, None, datetime.now())
        self.tournament_id = 0
        self.player_id = 0
        self.round_id = 0

    def __call__(self):
        list_id_tournaments: list = self.tournament.return_id_all_table_with_players()
        list_tournaments: str = self.tournament.display_all_table_with_players()
        if list_tournaments is None:
            print('Vous n\'avez associé 8 joueurs à aucun tournoi')
        else:
            print(list_tournaments)
            try:
                self.tournament_id = int(
                    input('Pour quel tournoi voulez-vous générer les paires de joueurs (saisir le n°) ? '))
            except ValueError:
                self.tournament_id = 0
            if self.tournament_id not in list_id_tournaments:
                print("Vous n'avez pas saisi le n° d'un tournoi valable.")
            else:
                """ confirm that the last round is finish before created a new one """
                self.round.tournament = self.tournament_id
                self.round.name = self.tournament.return_rounds(self.tournament_id)[-1]
                self.round_id = self.round.search_id_round('tournament', self.tournament_id)
                if self.round.round_closed(self.round_id) is True:
                    if len(self.tournament.return_rounds(self.tournament_id)) < 4:
                        """ if there were already 4 rounds played, we forbid to create a new round """
                        list_players_tournament = self.tournament.return_players(self.tournament_id)
                        list_player: list = []
                        for player in list_players_tournament:
                            """ for the first round, we generate pairs based on the rank
                            for the next rounds, it's based on the points of the players """
                            if len(self.tournament.return_rounds(self.tournament_id)) == 0:
                                list_player.append(self.player.return_player_ranking(player))
                            else:
                                list_player.append(self.round.return_total_points_player_tournament(self.tournament_id,
                                                                                                    player))
                        self.tournament.rounds = self.tournament.return_rounds(self.tournament_id)
                        if self.tournament.rounds[-1] == 0:
                            self.tournament.rounds = []
                        self.tournament.rounds.append(int(self.round.name) + 1)
                        self.tournament.update_tournament_round(self.tournament_id, self.tournament.rounds)
                        if len(self.tournament.return_rounds(self.tournament_id)) == 1:
                            self.generate_pairs(list_players_tournament, list_player, False)
                        else:
                            self.generate_pairs(list_players_tournament, list_player, True)
                    else:
                        print("Le tournoi est terminé. Vous ne pouvez plus créer de nouveau round.")
                else:
                    print("Vous n'avez pas saisi tous les résultats des matchs pour le round en cours,"
                          " vous ne pouvez pas en créer un nouveau.")
        return TournamentMenuController

    def generate_pairs(self, list_players_tournament: list, list_player: list, sort_sens: bool = False):
        """ this method is called to associate the 8 players in 4 pairs,
        based on the rules of the Swiss tournament """
        if self.round.name == 0:
            for i in range(1, len(list_players_tournament), 2):
                players_couple: tuple = (list_players_tournament[i], list_players_tournament[i - 1])
                self.round.pairs.append(players_couple)
        else:
            old_list_players: list = self.round.return_old_pairs(self.round_id)
            """ with the list of the players of the last rounds, we can call the generate_pair method
            which give us the new pairs, different of the old one
            this new list of pairs of players id added to the pair attribut of the round instance """
            self.round.pairs.extend(self.round.generate_pair(list_player, old_list_players, sort_sens))
        print(self.round.pairs)
        self.round.name += 1
        self.round.data_hour_start = datetime.now()
        self.round.match = 0
        self.round.result = 0
        self.round.data_hour_end = None
        self.round.insert_round(self.round.serializ_round())


class EnterResultsController:
    """ after a match, the manager gives the results of it
     if one of the player wins, he has 1 point and the other 0
     if their is equality, both receive 0,5 point """

    def __init__(self):
        self.player = Player()
        self.tournament = Tournament(None, None, None)
        self.round = Round(None, None, datetime.now())
        self.match = Match(0, 0, 0, 0, 0, 0)
        self.tournament_id = 0
        self.player_id = 0
        self.round_name = 0
        self.round_id = 0
        self.match_id = 0

    def __call__(self):
        list_id_tournaments: list = self.tournament.return_id_all_table_with_players()
        list_tournaments: str = self.tournament.display_all_table_with_players()
        if list_tournaments is None:
            print('Vous n\'avez associé 8 joueurs à aucun tournoi')
        else:
            print(list_tournaments)
            try:
                self.tournament_id = int(input('Pour quel tournoi voulez-vous générer les paires de joueurs '
                                               '(saisir le n°) ? \n '))
            except ValueError:
                self.tournament_id = 0
            if self.tournament_id in list_id_tournaments:
                self.round_name = self.tournament.return_rounds(self.tournament_id)[-1]
                self.round_id = self.round.search_id_round('tournament', self.tournament_id)
                list_players: list = self.round.return_old_pairs(self.round_id)
                if len(list_players) == 4:
                    print(list_players)
                    player_score: int = 0
                    while player_score < 1 or player_score > 4:
                        player_score = int(
                            input("Pour quel paire de joueurs voulez-vous saisir les points (1, 2, 3 ou 4) ? \n"))
                    match_already: list = self.match.search_match('id_tournament', self.tournament_id)
                    for m_already in match_already:
                        if (m_already['player_1'], m_already['player_2']) == \
                                (list_players[player_score - 1][0], list_players[player_score - 1][1]) and \
                                m_already['round_name'] == self.round_name:
                            print('Vous avez déjà indiqué le gagnant de ce match')
                            return TournamentMenuController
                    winner: int = int(input("Qui est le gagant du match (n° du joueur ou 0 si match nul) ? \n "))
                    self.match.id_tournament = self.tournament_id
                    self.match.round_name = self.round_name
                    self.match.player_1 = list_players[player_score - 1][0]
                    self.match.player_2 = list_players[player_score - 1][1]
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
            else:
                print("Vous n'avez pas saisi le n° d'un tournoi valable.")
        return TournamentMenuController


class PlayersMenuController:
    """ controller for the player menu which allow to create and delete players and change their rank """

    def __init__(self):
        self.menu = Menu()
        self.view = HomeMenuView(self.menu)

    def __call__(self) -> str:
        self.menu.clear()
        self.menu.add("auto", "Créer", PlayersCreate)
        self.menu.add("auto", "Modifier Classement", RankingMenuController)
        self.menu.add("r", "Retour", HomeMenuController)

        user_choice = self.view.get_user_choice("Players")
        """ return of the next controller """
        return user_choice.handler


class PlayersCreate:
    """ controller to add players by given their name, surname, birthdate and sex"""
    format = "%d/%m/%Y"

    def __init__(self):
        """ we add the player view and player model to the controller """
        self.player = Player()
        self.player_view = PlayerView()
        self.player_id = None
        self.tournament = Tournament(None, None, None)

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
    def is_answer_empty(answer: str = None) -> bool:
        """ check if the user has written something """
        if answer == "":
            return True
        else:
            return False

    def __call__(self, nb_players: int = 1):
        """ we ask the questions about the players and we add them to the instance of players
        and insert them into the Tinydb table Player
         we loop those questions for all the players we want to add """
        for _ in range(1, nb_players + 1):
            input_player = []
            questions_player = [self.player_view.quest_name, self.player_view.quest_last_name,
                                self.player_view.quest_birth_date, self.player_view.quest_sex]
            for quest in questions_player:
                good_answer = False
                self.player_view.player_ask(quest)
                answer: str or None = None
                while not good_answer:
                    answer = input('>> ').strip()
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
    """ the manager can change the rank of any player """

    def __init__(self):
        self.player = Player()
        self.player_id = 0

    def __call__(self, tournament_id: int = 0):
        print("ID".ljust(4) + ' ' + "Prénom".ljust(15) + ' ' + "Nom".ljust(15) + ' ' +
              "Clas.".ljust(4))
        print(self.player.display_all_table(True))
        player_modif_rank: int = int(input("Pour quel joueur voulez-vous modifier le classement (saisir son n°) ? \n"))
        new_rank: int = int(input("Quel est son nouveau classement ? \n"))
        self.player.update_player_ranking(player_modif_rank, new_rank)
        return PlayersMenuController


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
    """ report on all the players even they haven't played
    we can display them sorted by ranking or by name """

    def __init__(self):
        self.player = Player()

    def __call__(self):
        """ displaying the actors according to the sort chosen """
        try:
            sorting_order: int = int(input('Voulez-vous trier les acteurs par ordre alphabétique (1) '
                                           'ou en fonction du rang (2) ? '))
        except Exception:
            sorting_order = 1
        if sorting_order not in (1, 2):
            sorting_order = 1
        print("ID".ljust(4) + ' ' + "Prénom".ljust(15) + ' ' + "Nom".ljust(15) + ' ' + "Date Naiss.".ljust(14) + ' ' +
              "Sexe".ljust(4) + ' ' + "Clas.".ljust(4))
        print(self.player.display_all_table_all_data(sorting_order))

        return ReportMenuController


class PlayersReportController:
    """ report on the players of a chosen tournament
    we can display them sorted by ranking or by name """

    def __init__(self):
        self.player = Player()
        self.tournament = Tournament(None, None, None)

    def __call__(self):
        id_tournament: int = 0
        print(self.tournament.display_all_table())
        try:
            id_tournament = int(input('Pour quel tournoi voulez-vous afficher les joueurs (saisir le n°) ?'))
            """ displaying the players according to the sort chosen """
        except Exception:
            PlayersReportController()
        try:
            sorting_order: int = int(input('Voulez-vous trier les acteurs par ordre alphabétique (1) '
                                           'ou en fonction du rang (2) ? '))
        except Exception:
            sorting_order = 1
        if sorting_order not in (1, 2):
            sorting_order = 1

        print("Prénom".ljust(15) + ' ' + "Nom".ljust(15) + ' ' + "Date Naiss.".ljust(14) + ' ' +
              "Sexe".ljust(4) + ' ' + "Clas.".ljust(4) + ' ' + "Points".ljust(4))
        liste_players: list = self.tournament.return_players(id_tournament)
        print(self.player.display_all_table_all_data_for_tournament(liste_players, sorting_order, id_tournament))
        return ReportMenuController


class TournamentsReportController:
    """ report of the different tournaments """

    def __init__(self):
        self.tournament = Tournament(None, None, None)

    def __call__(self):
        """ displaying the tournaments """
        print("Nom".ljust(20) + "place".ljust(20) + "date".ljust(14) + "date fin".ljust(14) +
              "rounds".ljust(14) + "contrôle du temps".ljust(20) + "description".ljust(30))
        print(self.tournament.display_all_tournaments())
        return ReportMenuController


class RoundsReportController:
    """ report of the different rounds of a chosen tournament """

    def __init__(self):
        self.tournament = Tournament()
        self.round = Round()

    def __call__(self):
        id_tournament: int = 0
        print(self.tournament.display_all_table())
        try:
            id_tournament = int(input('Pour quel tournoi voulez-vous afficher les rounds (saisir le n°) ?'))
        except Exception:
            ReportMenuController()
        """ displaying the rounds """
        print("Nom".ljust(8) + "date/heure deb".ljust(20) + "date/heure fin".ljust(20) +
              "matchs".ljust(14))
        print(self.round.display_all_rounds(id_tournament))
        return ReportMenuController


class MatchsReportController:
    """ report of the match of a chosen tournament """

    def __init__(self):
        self.player = Player()
        self.tournament = Tournament(None, None, None)
        self.round = Round(None, None, None)
        self.match = Match(None, None, None, None, None, None)

    def __call__(self):
        id_tournament: int = 0
        print(self.tournament.display_all_table())
        try:
            id_tournament = int(input('Pour quel tournoi voulez-vous afficher les matchs (saisir le n°) ?'))
        except Exception:
            ReportMenuController()
        """ displaying the matchs """
        print("Round".ljust(8) + "Match".ljust(8) + "1er Joueur".ljust(15) + "Points".ljust(8) +
              "2e Joueur".ljust(15) + "Points".ljust(8))
        print(self.match.display_all_matchs(id_tournament))
        return ReportMenuController


class ExitMenuController:
    def __call__(self):
        quit()
