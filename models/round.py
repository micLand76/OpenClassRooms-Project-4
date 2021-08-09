from models.match import Match
from tinydb import TinyDB, where
from models.access_db import DbManag


class Round:
    """ Class to create a Round witch is composed by many matchs
        It allows also to generate pairs of players with the Swiss method"""
    round = DbManag.db.table('round')

    def __init__(self, name, data_hour_start, data_hour_end):
        self.name = name
        self.data_hour_start = data_hour_start
        self.data_hour_end = data_hour_end
        self.match = []
        self.result = None

    def create_round(self):
        pass

    def generate_pair(self, round_number):
        # generate pair of players with the Tournament Swiss system
        pass

    def insert_round(self):
        self.round.insert({'name': self.name, 'match': self.match, 'result': self.result,
                           'data_hour_start': self.data_hour_start, 'data_hour_end': self.data_hour_end})

    def search_round(self, field='name', value=''):
        results = self.round.search(where(field) == value)  # returns a list
        for res in results:
            return res  # type: TinyDB.database.Document
            # print(res.city) # Not allowed!
            # print(res[field])

    def search_round_by_id(self, value=1) -> str:
        return 'le round ' + str(self.round.get(doc_id=value))

    def update_player(self, id_round='', field='name', value=''):
        self.round.update({field: value}, DbManag.User.id_round == id_round)
