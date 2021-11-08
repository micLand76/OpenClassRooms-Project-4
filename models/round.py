import time
from datetime import datetime
from itertools import chain
from tinydb import TinyDB, where
from models.access_db import DbManag
from models.match import Match


class Round:
    """ Class to create a Round witch is composed by many matchs
        It allows also to generate pairs of players with the Swiss method"""
    round = DbManag.db.table('round')

    def __init__(self, tournament, name, data_hour_start, data_hour_end: datetime = None):
        self.match = Match(0, 0, 0, 0, 0, 0)
        self.tournament: int = tournament
        self.name = name
        self.data_hour_start: datetime = data_hour_start
        self.data_hour_end: datetime = data_hour_end
        self.match_id = []
        self.pairs = []

    def serializ_round(self) -> dict:
        return {'tournament': self.tournament,
                'name': self.name,
                'data_hour_start': self.data_hour_start,
                'data_hour_end': self.data_hour_end,
                'match_id': self.match_id,
                'pairs': self.pairs}

    def insert_round(self, round_serializ):
        self.round.insert(round_serializ)

    def round_closed(self, round_id) -> bool:
        """ to check if the round is closed we look at the data_hour_end: it's empty if not finished """
        data_round = self.round.get(doc_id=round_id)
        if data_round is not None:
            data_hour_end = data_round['data_hour_end']
            if data_hour_end is None:
                return False
            else:
                return True
        else:
            return True

    def return_old_pairs(self, round_id: int) -> list:
        """ return the pairs for a round given in parameter
        the pairs are returned in tuple nd the 4 tuple in a list """
        data_round = self.round.get(doc_id=round_id)
        round_pairs: list = data_round['pairs']
        return_pairs: list = []
        for i in range(len(round_pairs)):
            return_pairs.append(tuple(round_pairs[i - 1]))
        return return_pairs

    def search_id_round(self, field='name', value: int = 0) -> int:
        """ search the id of the round by giving a value of a field
        if the field given id the tournament_id, then we can return the last
        round_id with a loop on the results so the last result will be the last round
        played"""
        results = self.round.search(where(field) == value)
        res_id: int = 0
        for res in results:
            res_id = res.doc_id
        return res_id

    def return_matchs_id(self, round_id: int) -> list:
        """ return the matchs for a round given in parameter
        the matchs are returned in a list """
        data_round = self.round.get(doc_id=round_id)
        round_matchs: list = data_round['match_id']
        return_matchs: list = []
        for i in range(len(round_matchs)):
            return_matchs.append(round_matchs[i - 1])
        return return_matchs

    def update_round(self, id_round='', field='name', value=''):
        self.round.update({field: value}, doc_ids=[id_round])

    def delete_round(self, id_tournament: int):
        self.round.remove(where('tournament') == id_tournament)

    def pair_already_played(self, list_players: list, old_list_players: list, pair_players: tuple,
                            test_already_apaired: True):
        """ verify that this combination isn't already existing """
        if self.player_already_apaired(list_players, pair_players) is True:
            if test_already_apaired is True:
                return True
            else:
                return pair_players
        else:
            old_list = old_list_players
            return any(old_list[j] in [pair_players, pair_players[::-1]] for j in range(4))

    @staticmethod
    def player_already_apaired(list_players: list, pair_players: tuple) -> bool:
        """ verify that a player isn't yet in the list of already paired players """
        if pair_players[0] in list(chain.from_iterable(list_players)) or \
                pair_players[1] in list(chain.from_iterable(list_players)):
            return True
        else:
            return False

    def return_total_points_player_round(self, tournament_id: int, round_name: int, player_id: int) -> int:
        match_already = self.match.search_match('id_tournament', tournament_id)
        total_points = 0
        for m_already in match_already:
            if m_already['round_name'] == round_name:
                if m_already['player_1'] == player_id:
                    total_points += m_already['result_1']
                elif m_already['player_2'] == player_id:
                    total_points += m_already['result_2']
        return total_points

    def return_total_points_player_tournament(self, tournament_id: int, player_id: int) -> dict:
        match_already = self.match.search_match('id_tournament', tournament_id)
        total_points = 0
        for m_already in match_already:
            if m_already['player_1'] == player_id:
                total_points += m_already['result_1']
            elif m_already['player_2'] == player_id:
                total_points += m_already['result_2']
        return {'id': player_id, 'rank': total_points}

    def generate_pair(self, list_player: list, old_list_players: list, sort_sens: bool = False):
        """ to generate pairs we need to be sure that the couple hasn't played yet
        and if the 3 first couples are generated but the 4th had already played so we need to broke the
        3 first pairs """
        pairs: list = []
        list_player = sorted(list_player, key=lambda t: (t['rank'] == 0, t['rank']), reverse=sort_sens)
        i = 0
        number_tours = 4
        while i < number_tours:
            players_couple: tuple = (list_player[i]['id'], list_player[i + 4]['id'])
            for _ in range(4):
                num_player = 3
                while self.pair_already_played(pairs, old_list_players, players_couple,
                                               True) is True and num_player < 7:
                    num_player += 1
                    players_couple = (list_player[i]['id'], list_player[num_player]['id'])

                """ if the last pair already exists, we make a new pair and change others pairs """
                if self.pair_already_played(pairs, old_list_players, players_couple, True) is True and i == 3:
                    for player_associate in range(7, 3, -1):
                        players_couple = (list_player[3]['id'], list_player[player_associate]['id'])
                        return_pair_already_played = self.pair_already_played(pairs, old_list_players, players_couple,
                                                                              False)
                        if return_pair_already_played is not True:
                            i = -1
                            number_tours = 3
                            pairs.clear()
                            break
                    break

            pairs.append(players_couple)
            i += 1

        return pairs

    def rounds_for_tournament(self, id_tournament: int):
        return self.round.search(where('tournament') == id_tournament)

    def display_all_rounds(self, id_tournament: int) -> str:
        all_rounds = self.rounds_for_tournament(id_tournament)
        nb_rounds = len(all_rounds)
        all_rounds_return: str = ""
        dte_hour_end: str = ""
        for i in range(nb_rounds):
            data_hour_end: datetime = all_rounds[i].get('data_hour_end', None)
            if data_hour_end is not None:
                data_hour_end = data_hour_end.strftime('%Y-%m-%d %H:%M')
                dte_hour_end = str(data_hour_end)
            all_rounds_return += str(all_rounds[i].get('name')).capitalize().ljust(8) + \
                                 str(all_rounds[i].get('data_hour_start').strftime('%Y-%m-%d %H:%M')).ljust(20) + \
                                 dte_hour_end.ljust(20) + \
                                 str(all_rounds[i].get('match_id')).strip('[]').ljust(14) + "\n"
        return all_rounds_return
