from tinydb import where

from models.access_db import DbManag
import models


class Match:
    """ Class to create a Match witch contain 2 players and their results"""
    match = DbManag.db.table('match')

    def __init__(self, id_tournament: int or None, round_name: int or None, player_1: int or None,
                 result_1: int or None, player_2: int or None, result_2: int or None):
        self.player = models.Player()
        self.id_tournament: int = id_tournament
        self.round_name: int = round_name
        self.player_1: int = player_1
        self.result_1: int = result_1
        self.player_2: int = player_2
        self.result_2: int = result_2

    def attribut_points(self, winner: int):
        """ based on the rules given to attribute points after a match """
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
        """ after serialized the data, we can insert them into the database """
        self.match.insert({'id_tournament': self.id_tournament, 'round_name': self.round_name,
                           'player_1': self.player_1, 'result_1': self.result_1,
                           'player_2': self.player_2, 'result_2': self.result_2})

    def search_id_match(self, field: str = 'name', value: int = 0) -> int:
        """ search the id of the match by giving a value of a field
        if the field given id the tournament_id, then we can return the last
        match_id with a loop on the results so the last result will be the last match
        played"""
        results = self.match.search(where(field) == value)
        res_id: int = 0
        for res in results:
            res_id = res.doc_id
        return res_id

    def search_match(self, field: str, value: int) -> list:
        """ used to know the id for all the matchs played in the round """
        results = self.match.search(where(field) == value)
        for r in results:
            r['id'] = r.doc_id
        return results

    def display_all_matchs(self, id_tournament: int) -> str:
        """ displaying the matchs for a tournament given for the reports
        we separate the matchs of each round """
        all_matchs: list = self.search_match('id_tournament', id_tournament)
        nb_matchs: int = len(all_matchs)
        all_matchs_return: str or None = None
        if nb_matchs > 0:
            round_last: int = all_matchs[0].get('round_name')
            for i in range(nb_matchs):
                if all_matchs[i].get('round_name') != round_last:
                    all_matchs_return += "\n"
                    round_last = all_matchs[i].get('round_name')
                player1: str = self.player.search_instance_player_by_id(
                    all_matchs[i].get('player_1'), id_tournament)['name']
                player2: str = self.player.search_instance_player_by_id(
                    all_matchs[i].get('player_2'), id_tournament)['name']
                match_return: str = str(all_matchs[i].get('round_name')).capitalize().ljust(8) + \
                    str(all_matchs[i].get('id')).capitalize().ljust(8) + \
                    player1.ljust(15) + \
                    str(all_matchs[i].get('result_1')).ljust(8) + \
                    player2.ljust(15) + \
                    str(all_matchs[i].get('result_2')).ljust(8) + "\n"
                if all_matchs_return is None:
                    all_matchs_return = match_return
                else:
                    all_matchs_return += match_return
        else:
            print('Il n\'y a pas encore de match pour ce tournoi')
        return all_matchs_return
