from datetime import datetime
from tinydb import where

from models.access_db import DbManag


class Tournament:
    """ Class to create a Tournament witch is composed by many round
        and contain the rank of the players"""
    tournament = DbManag.db.table('tournament')

    def __init__(self, name: str = None, place: str = None, description: str = None,
                 time_control: str = 'Bullet', tour_number: int = 4, tourn_date: datetime = datetime.now()):
        """ attributes we need to create a tournament """
        self.name: str = name
        self.place: str = place
        self.tourn_date: datetime = tourn_date
        self.tourn_date_end: datetime = None
        self.tour_number: int = tour_number
        self.time_control: str = time_control
        self.description: str = description
        self.rounds: list = []
        self.players: list = []

    def serializ_tournament(self) -> dict:
        """ to insert the data into tinydb, they need to be serialized in a dict """
        return {'name': self.name,
                'place': self.place,
                'tourn_date': datetime.now(),
                'tourn_date_end': None,
                'rounds': self.rounds,
                'players': self.players,
                'time_control': self.time_control,
                'description': self.description}

    def insert_tournament(self, tournament_serializ: dict):
        """ after serialized the data, we can insert them into the database """
        self.tournament.insert(tournament_serializ)

    def update_tournament(self, id_tournament: list):
        """ once we have attribute the players to the tournament we can update the database """
        self.tournament.update({'players': self.players}, doc_ids=id_tournament)

    def update_tournament_round(self, id_tournament: int, value: list):
        """ once we have attribute the rounds list to the tournament we can update the database """
        self.tournament.update({'rounds': value}, doc_ids=[id_tournament])

    def update_tournament_date_end(self, id_tournament: int, value: datetime):
        """ once we have attribute the date end to the tournament we can update the database """
        self.tournament.update({'tourn_date_end': value}, doc_ids=[id_tournament])

    def search_id_tournament(self, field: str = 'name', value: str = None) -> int:
        """ search the id of the tournament by giving a value of a field """
        results = self.tournament.search(where(field) == value)
        for res in results:
            return res.doc_id

    def display_all_table(self) -> str:
        """ to display the list of the tournaments """
        all_tournaments = self.tournament.all()
        nb_tournaments = len(self.tournament)
        return ''.join('Tournoi ' + str(self.search_id_tournament('name', all_tournaments[i].get('name'))) + ' ' +
                       all_tournaments[i].get('name') + " (" + all_tournaments[i].get('place') + ") \n"
                       for i in range(nb_tournaments))

    def display_all_table_with_players(self) -> str:
        """ to display only tournaments with 8 players associate """
        all_tournaments = self.tournament.all()
        list_tournaments: str or None = None
        for id_tournament in all_tournaments:
            nb_players: list = id_tournament.get('players')
            if len(nb_players) == 8:
                lgn_tournament = 'Tournoi ' + str(self.search_id_tournament('name', id_tournament.get('name'))) + \
                                 ' ' + id_tournament.get('name') + " (" + id_tournament.get('place') + ") \n"
                if list_tournaments is None:
                    list_tournaments = lgn_tournament
                else:
                    list_tournaments += lgn_tournament
        return list_tournaments

    def return_id_all_table_with_players(self) -> list:
        """ return a list of tournaments with 8 players
        it's useful to check if a tournament has already 8 players associated """
        all_tournaments = self.tournament.all()
        list_id_tournaments: list = []
        for id_tournament in all_tournaments:
            nb_players: list = id_tournament.get('players')
            if len(nb_players) == 8:
                list_id_tournaments.append(self.search_id_tournament('name', id_tournament.get('name')))
        return list_id_tournaments

    def display_all_tournaments(self) -> str:
        """ displaying the list of tournaments with all informations
        useful for the reports """
        all_tournaments = self.tournament.all()
        nb_tournaments = len(self.tournament)
        list_tournament: str = ""
        date_end: str = str(None)
        for i in range(nb_tournaments):
            if all_tournaments[i].get('tourn_date_end') is None or \
                    type(all_tournaments[i].get('tourn_date_end')) is str:
                date_end = " "
            else:
                date_end = str(all_tournaments[i].get('tourn_date_end').strftime(None, '%Y-%m-%d'))
            list_tournament += str(all_tournaments[i].get('name'))[:19].capitalize().ljust(20) + \
                               str(all_tournaments[i].get('place'))[:19].capitalize().ljust(20) + \
                               str(all_tournaments[i].get('tourn_date').strftime('%Y-%m-%d')).ljust(14) + \
                               date_end.ljust(14) + \
                               str(all_tournaments[i].get('rounds')[0]).ljust(14) + \
                               str(all_tournaments[i].get('time_control')).capitalize().ljust(20) + \
                               str(all_tournaments[i].get('description')).capitalize().ljust(30) + "\n"
        return list_tournament

    def return_players(self, id_tournament: int) -> list:
        """ for a given tournament we want to know the list of its players """
        all_tournaments = self.tournament.all()
        return list(all_tournaments[id_tournament - 1].get('players'))

    def return_nb_players_per_tournament(self, id_tournament: int) -> int:
        """ to check if a tournament has already 8 players associated """
        data_tournament = self.tournament.get(doc_id=id_tournament)
        nb_players: list = data_tournament['players']
        return len(nb_players)

    def return_rounds(self, id_tournament: int) -> list:
        """ when we create a new round we need to know the last round created """
        all_tournaments = self.tournament.all()
        last_round: list = all_tournaments[int(id_tournament) - 1]['rounds']
        return last_round
