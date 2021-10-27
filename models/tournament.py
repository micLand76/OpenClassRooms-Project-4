import datetime
from json import JSONEncoder
from tinydb import TinyDB, where

from models.access_db import DbManag


# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


class Tournament:
    """ Class to create a Tournament witch is composed by many round
        and contain the rank of the players"""
    tournament = DbManag.db.table('tournament')

    def __init__(self, name, place, description, time_control='Bullet', tour_number=4,
                 tourn_date=datetime.datetime.now()):
        self.name = name
        self.place = place
        self.tourn_date = tourn_date
        self.tour_number = tour_number
        self.time_control = time_control
        self.description = description
        self.rounds = []
        self.players = []

    def serializ_tournament(self) -> dict:
        return {'name': self.name,
                'place': self.place,
                'tourn_date': datetime.datetime.now(),
                'rounds': self.rounds,
                'players': self.players,
                'time_control': self.time_control,
                'description': self.description}

    def insert_tournament(self, tournament_serializ):
        self.tournament.insert(tournament_serializ)

    def update_tournament(self, id_tournament: list, value):
        # il faut ajouter à une liste et non comme une chaine
        # val = ''.join(value[i] + ', ' for i in range(len(value)))
        # for i in range(len(value)):
        # self.players.append(value[i])
        self.tournament.update({'players': self.players}, doc_ids=id_tournament)

    def update_tournament_round(self, id_tournament: int, value: list):
        self.tournament.update({'rounds': value}, doc_ids=[id_tournament])

    def search_id_tournament(self, field='name', value=''):
        """ search the id of the tournament by giving a value of a field """
        results = self.tournament.search(where(field) == value)  # returns a list
        for res in results:
            return res.doc_id

    def display_all_table(self) -> str:
        all_tournaments = self.tournament.all()
        nb_tournaments = len(self.tournament)
        return ''.join('Tournoi ' + str(self.search_id_tournament('name', all_tournaments[i].get('name'))) + ' ' +
                       all_tournaments[i].get('name') + " (" + all_tournaments[i].get('place') + ") \n"
                       for i in range(nb_tournaments))

    def display_all_table_with_players(self) -> str:
        all_tournaments = self.tournament.all()
        list_tournaments = ''
        for id_tournament in all_tournaments:
            nb_players: list = id_tournament.get('players')
            if len(nb_players) == 8:
                list_tournaments += 'Tournoi ' + str(self.search_id_tournament('name', id_tournament.get('name'))) + \
                                    ' ' + id_tournament.get('name') + " (" + id_tournament.get('place') + ") \n"
        return list_tournaments

    def display_all_tournaments(self) -> str:
        all_tournaments = self.tournament.all()
        nb_tournaments = len(self.tournament)
        return ''.join(str(all_tournaments[i].get('name')).capitalize().ljust(15) +
                       str(all_tournaments[i].get('place')).capitalize().ljust(14) +
                       str(all_tournaments[i].get('tourn_date').strftime('%Y-%m-%d')).ljust(14) +
                       str(all_tournaments[i].get('rounds')[0]).ljust(14) +
                       str(all_tournaments[i].get('time_control')).capitalize().ljust(20) +
                       str(all_tournaments[i].get('description')).capitalize().ljust(20) + "\n"
                       for i in range(nb_tournaments))

    def return_players(self, id_tournament: int) -> list:
        all_tournaments = self.tournament.all()
        return list(all_tournaments[id_tournament - 1].get('players'))

    def return_nb_players_per_tournament(self, id_tournament: int) -> int:
        data_tournament = self.tournament.get(doc_id=id_tournament)
        nb_players: list = data_tournament['players']
        return len(nb_players)

    def return_rounds(self, id_tournament: int) -> list:
        all_tournaments = self.tournament.all()
        last_round: list = all_tournaments[int(id_tournament) - 1]['rounds']
        return last_round
