from itertools import chain


def pair_already_played(list_players: list, pair_players: tuple, test_already_apaired: True):
    """ verify that this combination isn't already existing """
    old_list = [(2, 11), (5, 1), (34, 8), (9, 3)]
    if player_already_apaired(list_players, pair_players) is True:
        if test_already_apaired is True:
            return True
        else:
            return pair_players
    else:
        return any(old_list[j] in [pair_players, pair_players[::-1]] for j in range(4))


def player_already_apaired(list_players: list, pair_players: tuple) -> bool:
    """ verify that a player isn't yet in the list of already paired players """
    if pair_players[0] in list(chain.from_iterable(list_players)) or \
            pair_players[1] in list(chain.from_iterable(list_players)):
        return True
    else:
        return False


list_player = [{'id': 2, 'rank': 1}, {'id': 3, 'rank': 7}, {'id': 5, 'rank': 2}, {'id': 34, 'rank': 3},
               {'id': 9, 'rank': 4}, {'id': 1, 'rank': 5}, {'id': 8, 'rank': 8}, {'id': 11, 'rank': 6}]
pairs = []

list_player = sorted(list_player, key=lambda t: t['rank'])
i = 0
number_tours = 4
while i < number_tours:
    players_couple: tuple = (list_player[i]['id'], list_player[i + 4]['id'])

    for j in range(4):
        num_player = 3
        while pair_already_played(pairs, players_couple, True) is True and num_player < 7:
            num_player += 1
            players_couple = (list_player[i]['id'], list_player[num_player]['id'])

        """ if the last pair already exists, we make a new pair and change others pairs """
        if pair_already_played(pairs, players_couple, True) is True and i == 3:
            for player_associate in range(7, 3, -1):
                players_couple = (list_player[3]['id'], list_player[player_associate]['id'])
                return_pair_already_played = pair_already_played(pairs, players_couple, False)
                if return_pair_already_played is not True:
                    i = -1
                    number_tours = 3
                    pairs.clear()
                    break
            break
            """ find the player who was associated with the player which is now associate with the player 3 """
            """result = list(filter(lambda x: x[1] == return_pair_already_played[1], pairs))
            for p in range(3):
                if pairs[p][0] == result[0]:
                    print('pair', p)
                    break"""

    pairs.append(players_couple)
    i += 1

print(pairs)
