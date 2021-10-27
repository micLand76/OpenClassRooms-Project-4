from models.access_db import DbManag
from tinydb import TinyDB, where
from operator import itemgetter, attrgetter


class Player:
    """ Class to create a Player with his attributes and to give his rank"""
    player = DbManag.db.table('player')
    number_of_player = 0

    def __init__(self, name='', last_name='', birth_date='', sex='M'):
        self.name = name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex
        self.rank = 0

    def serializ_player(self) -> dict:
        return {'name': self.name,
                'last_name': self.last_name,
                'birth_date': self.birth_date,
                'sex': self.sex,
                'ranking': self.rank}

    def insert_player(self, player_serializ):
        self.player.insert(player_serializ)

    def number_of_players(self) -> int:
        return len(self.player)

    def return_player_ranking(self, player_id: int) -> dict:
        data_player = self.player.get(doc_id=player_id)
        return {'id': player_id, 'rank': data_player['ranking']}

    def search_id_player(self, field='name', value=''):
        """ search the id of the player by giving a value of a field """
        results = self.player.search(where(field) == value)  # returns a list
        for res in results:
            return res.doc_id

    def search_instance_player_by_id(self, value=1):
        data_player = self.player.get(doc_id=value)
        player = Player(data_player['name'], data_player['last_name'], data_player['birth_date'], data_player['sex'])
        player.rank = data_player['ranking']
        return {'name': player.name,
                'last_name': player.last_name,
                'birth_date': player.birth_date,
                'sex': player.sex,
                'ranking': player.rank}

    def display_all_table(self):
        all_players = self.player.all()
        nb_players = len(self.player)
        return ''.join('Joueur ' + str(self.search_id_player('name', all_players[i].get('name'))) + ' ' +
                       all_players[i].get('last_name') + " " + all_players[i].get('name') + " \n"
                       for i in range(nb_players-1))

    def display_all_table_all_data(self, sorting_order=1):
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

    def display_all_table_all_data_for_tournament(self, list_players: list, sorting_order=1):
        nb_players = len(list_players)
        instance_players = []
        for i in range(nb_players):
            instance_players.append(self.search_instance_player_by_id(list_players[i]))
        if sorting_order == 1:
            all_players = sorted(instance_players, key=lambda k: k['name'].capitalize())
        else:
            all_players = sorted(instance_players, key=lambda k: (k['ranking'] == 0, k['ranking']))
        player_list = ''
        for i in range(nb_players):
            player_list += all_players[i]["last_name"].capitalize().ljust(15) + " " + \
                           all_players[i]["name"].capitalize().ljust(15) + " " + \
                           str(all_players[i]["birth_date"]).ljust(14) + " " + \
                           all_players[i]["sex"].ljust(4) + " " + \
                           str(all_players[i]["ranking"]).ljust(4) + " \n"
        return player_list
