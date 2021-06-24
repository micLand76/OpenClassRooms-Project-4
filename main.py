from tinydb import TinyDB, Query, where
from pprint import pprint

db = TinyDB('db.json')

tournament = db.table('tournament')
round = db.table('round')
match = db.table('match')
player = db.table('player')

tournament.insert({'name': '', 'place': '', 'tours_number': '', 'rounds': '', \
                  'players': '', 'time_control': '', 'description': ''})
round.insert({'name': '', 'match': '', 'result': '', 'date_hour_begin': '', \
                  'date_hour_end': ''})
match.insert({'ID': '', 'player1_result1': '', 'player2_result2': ''})
player.insert({'ID_player': '', 'name': '', 'last_name': '', 'birth_date': '', \
                  'sex': '', 'ranking': ''})

pprint(tournament.all())