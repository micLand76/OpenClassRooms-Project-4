# list_player = [(2, 1), (3, 5), (5, 2), (34, 3), (9, 4), (1, 7), (8, 8), (11, 6)]
import itertools
from itertools import chain


def already_played(pair_players: tuple) -> bool:
    """ verify that this combination isn't already existing """
    old_list = [(2, 1), (5, 11), (34, 8), (9, 3)]
    return any(old_list[j] in [pair_players, pair_players[::-1]] for j in range(4))


def already_apaired(list_players: list, pair_players: tuple) -> bool:
    """ verify that a player isn't yet in the list of already apaired players """
    print(pair_players[0], pair_players[1], list(chain.from_iterable(list_players)))
    if pair_players[0] in list(chain.from_iterable(list_players)) or \
            pair_players[1] in list(chain.from_iterable(list_players)):
        return True
    else:
        return False


list_player = [{'id': 2, 'rank': 1}, {'id': 3, 'rank': 5}, {'id': 5, 'rank': 2}, {'id': 34, 'rank': 3},
               {'id': 9, 'rank': 4}, {'id': 1, 'rank': 7}, {'id': 8, 'rank': 8}, {'id': 11, 'rank': 6}]
pairs = []

print(sorted(list_player, key=lambda t: t['rank']))
list_player = sorted(list_player, key=lambda t: t['rank'])
i = 0
while i < 4:
    players_couple: tuple = (list_player[i]['id'], list_player[i + 4]['id'])
    ''' initialization of the flag exist to manage the case of an already existing tuple '''
    exists = False
    for j in range(4):
        if already_played(players_couple) is True:
            print('paire existante:', players_couple)

            ''' if the tuple is already existing, we associate the next player with the player i '''
            if i < 3:
                players_couple = (list_player[i]['id'], list_player[i + 5]['id'])
                print('nouvelle paire:', players_couple)

    if not exists:
        if not already_apaired(pairs, players_couple):
            pairs.append(players_couple)
            print('paire ajoutée:', players_couple)
        else:
            print(players_couple, 'existe déjà')
    i += 1

for a in pairs:
    print(a)

print(pairs)
