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
        self.rounds = name
        self.players = []
        self.rounds = []

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

    def search_tournament(self, field='name', value=''):
        results = self.tournament.search(where(field) == value)  # returns a list
        for res in results:
            return res  # type: TinyDB.database.Document
            # print(res.city) # Not allowed!
            # print(res[field])

    def search_tournament_by_id(self, value=1) -> str:
        return 'le tournoi ' + str(self.tournament.get(doc_id=value))

    def update_tournament(self, id_tournament='', field='name', value=''):
        self.tournament.update({field: value}, DbManag.User.id_tournament == id_tournament)
