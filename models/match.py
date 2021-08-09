from tinydb import TinyDB, where
from models.access_db import DbManag


class Match:
    """ Class to create a Match witch contain 2 players and their results"""
    match = DbManag.db.table('match')

    def __init__(self, player_1, player_2):
        self.id_match = 0
        self.player_1 = player_1
        self.player_2 = player_2
        self.result_1 = 0
        self.result_2 = 0

    def attribut_points(self, winner):
        if winner == self.player_1:
            self.result_1 = 1
        elif winner == self.player_2:
            self.result_2 = 1
        else:
            self.result_1 = 1 / 2
            self.result_2 = 1 / 2

    def create_match(self):
        pass

    def insert_match(self, name='', last_name='', birth_date='', sex='M', ranking=''):
        self.match.insert({'name': name, 'last_name': last_name, 'birth_date': birth_date,
                           'sex': sex, 'ranking': ranking})

    def search_match(self, field='name', value=''):
        results = self.match.search(where(field) == value)  # returns a list
        for res in results:
            return res  # type: TinyDB.database.Document
            # print(res.city) # Not allowed!
            # print(res[field])

    def search_match_by_id(self, value=1) -> str:
        return 'le joueur ' + str(self.match.get(doc_id=value))

    def update_match(self, id_match='', field='name', value=''):
        self.match.update({field: value}, DbManag.User.id_match == id_match)
