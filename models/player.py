from models.access_db import DbManag


class Player:
    """ Class to create a Player with his attributes and to give his rank"""
    player = DbManag.db.table('player')

    def __init__(self, name='', last_name='', birth_date='', sex='M'):
        self.name = name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex
        self.rank = 0

    def update_ranking(self, rank):
        self.rank = rank

    def serializ_player(self) -> dict:
        return {'name': self.name,
                'last_name': self.last_name,
                'birth_date': self.birth_date,
                'sex': self.sex,
                'ranking': self.rank}

    def insert_player(self, player_serializ):
        self.player.insert(player_serializ)

    def search_player(self, field='name', value=''):
        """ to find data by giving the field and a value """
        return DbManag.search_data(self.player, field, value)

    def search_player_by_id(self, value=1) -> str:
        return 'le joueur ' + str(self.player.get(doc_id=value))

    def update_player(self, id_player='', field='name', value=''):
        self.player.update({field: value}, DbManag.User.id_player == id_player)
