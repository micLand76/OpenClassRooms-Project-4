from tinydb import TinyDB, where
from models.access_db import DbManag


class Match:
    """ Class to create a Match witch contain 2 players and their results"""
    match = DbManag.db.table('match')

    def __init__(self, id_tournament, round_name, player_1, result_1, player_2, result_2):
        self.id_tournament = id_tournament
        self.round_name = round_name
        self.player_1 = player_1
        self.result_1 = result_1
        self.player_2 = player_2
        self.result_2 = result_2

    def attribut_points(self, winner: int):
        if winner == self.player_1:
            self.result_1 = 1
            self.result_2 = 0
        elif winner == self.player_2:
            self.result_2 = 1
            self.result_1 = 0
        else:
            self.result_1 = 1 / 2
            self.result_2 = 1 / 2

    def insert_match(self):
        self.match.insert({'id_tournament': self.id_tournament, 'round_name': self.round_name,
                           'player_1': self.player_1, 'result_1': self.result_1,
                           'player_2': self.player_2, 'result_2': self.result_2})

    def search_id_match(self, field='name', value: int = 0) -> int:
        """ search the id of the match by giving a value of a field
        if the field given id the tournament_id, then we can return the last
        match_id with a loop on the results so the last result will be the last match
        played"""
        results = self.match.search(where(field) == value)
        res_id: int = 0
        for res in results:
            res_id = res.doc_id
        return res_id

    def search_match(self, field='name', value=''):
        results = self.match.search(where(field) == value)  # returns a list
        return results
