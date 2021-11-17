from datetime import datetime
from models.access_db import DbManag
from tinydb import where

import models


class Player:
    """ Class to create a Player with his attributes and to give his rank"""
    player = DbManag.db.table('player')
    number_of_player = 0

    def __init__(self, name: str = None, last_name: str = None, birth_date: datetime = None, sex: str = 'M'):
        self.name = name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex
        self.rank = 0

    def serializ_player(self) -> dict:
        """ to insert the data into tinydb, they need to be serialized in a dict """
        return {'name': self.name,
                'last_name': self.last_name,
                'birth_date': self.birth_date,
                'sex': self.sex,
                'ranking': self.rank}

    def insert_player(self, player_serializ: dict):
        """ after serialized the data, we can insert them into the database """
        self.player.insert(player_serializ)

    def number_of_players(self) -> int:
        """ it's used to be sure that the tournament has its 8 players, before associate them """
        return len(self.player)

    def return_player_ranking(self, player_id: int) -> dict:
        """ for the first round, we associate the players based on their ranking
        so we need to know the rank for each player """
        data_player: list = self.player.get(doc_id=player_id)
        return {'id': player_id, 'rank': data_player['ranking']}

    def update_player_ranking(self, player_id: int, new_rank: int):
        """ allow to change the ranking of a player """
        self.player.update({'ranking': new_rank}, doc_ids=[player_id])

    def search_id_player(self, field: str = 'name', value: str = None) -> int:
        """ search the id of the player by giving a value of a field """
        results = self.player.search(where(field) == value)  # returns a list
        for res in results:
            return res.doc_id

    def player_exists(self, player_id: int) -> bool:
        """ for a player id given, we check if it exists """
        data_player = self.player.get(doc_id=player_id)
        if data_player is None:
            return False
        else:
            return True

    def search_instance_player_by_id(self, value: int = 1, tournament_id: int = 0) -> dict:
        """ used for the reports of the matchs and the players, for a tournament given """
        data_player = self.player.get(doc_id=value)
        player = Player(data_player['name'], data_player['last_name'], data_player['birth_date'], data_player['sex'])
        player.rank = data_player['ranking']
        player_points = self.return_total_points_player_tournament(tournament_id, value)
        return {'name': player.name,
                'last_name': player.last_name,
                'birth_date': player.birth_date,
                'sex': player.sex,
                'ranking': player.rank,
                'points': player_points}

    @staticmethod
    def return_total_points_player_tournament(tournament_id: int, player_id: int) -> int:
        """ used for the reports of the matchs and the players,
        to know the sum of the points of a player given for a tournament given"""
        match_already: list = models.Match.search_match(models.Match, 'id_tournament', tournament_id)
        total_points: int = 0
        for m_already in match_already:
            if m_already['player_1'] == player_id:
                total_points += m_already['result_1']
            elif m_already['player_2'] == player_id:
                total_points += m_already['result_2']
        return total_points

    def display_all_table(self, display_rank: bool = False) -> str:
        """ displaying all the actors saved in the database
        it's used for the report or to associate players to a tournament
        so there is two possibilities for the return: with or without the ranking """
        all_players = self.player.all()
        nb_players = len(self.player)
        if not display_rank:
            return ''.join('Joueur ' + str(self.search_id_player('name', all_players[i].get('name'))) + ' ' +
                           all_players[i].get('last_name') + " " + all_players[i].get('name') + " \n"
                           for i in range(nb_players - 1))
        else:
            return ''.join(str(self.search_id_player('name', all_players[i].get('name'))).ljust(4) + ' ' +
                           str(all_players[i].get('last_name')).ljust(15) + " " +
                           str(all_players[i].get('name')).ljust(15) + " " +
                           str(all_players[i].get('ranking')).ljust(4) + " \n"
                           for i in range(nb_players - 1))

    def display_all_table_all_data(self, sorting_order: int = 1) -> str:
        """ used for the report of the actors
        it can be sorted by the name or by the ranking """
        if sorting_order == 1:
            all_players = sorted(self.player.all(), key=lambda k: k['name'].capitalize())
        else:
            all_players = sorted(self.player.all(), key=lambda k: (k['ranking'] == 0, k['ranking']))
        nb_players = len(self.player)
        return ''.join(str(self.search_id_player("name", all_players[i].get("name"))).ljust(4) + ' ' +
                       all_players[i].get("last_name").capitalize().ljust(15) + " " +
                       all_players[i].get("name").capitalize().ljust(15) + " " +
                       str(all_players[i].get("birth_date")).ljust(14) + " " +
                       all_players[i].get("sex").ljust(4) + " " +
                       str(all_players[i].get("ranking")).ljust(4) + " \n"
                       for i in range(nb_players))

    def display_all_table_all_data_for_tournament(self, list_players: list, sorting_order: int = 1,
                                                  id_tournament: int = 0) -> str or None:
        """ used for the report of the players, for a tournament given,
        it can be sorted by the name or by the ranking """
        nb_players: int = len(list_players)
        instance_players: list = []
        for i in range(nb_players):
            instance_players.append(self.search_instance_player_by_id(list_players[i], id_tournament))
        if sorting_order == 1:
            all_players = sorted(instance_players, key=lambda k: k['name'].capitalize())
        else:
            all_players = sorted(instance_players, key=lambda k: (k['ranking'] == 0, k['ranking']))
        player_list: str or None = None
        for i in range(nb_players):
            player_record: str = all_players[i]["last_name"].capitalize().ljust(15) + " " + \
                           all_players[i]["name"].capitalize().ljust(15) + " " + \
                           str(all_players[i]["birth_date"]).ljust(14) + " " + \
                           all_players[i]["sex"].ljust(4) + " " + \
                           str(all_players[i]["ranking"]).ljust(4) + " " + \
                           str(all_players[i]["points"]).ljust(4) + " \n"
            if player_list is None:
                player_list = player_record
            else:
                player_list += player_record
        return player_list
