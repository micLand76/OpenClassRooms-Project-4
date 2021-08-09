class TournamentView:
    def __init__(self):
        """ questions to get the tournament's informations """
        self.quest_name = 'Veuillez saisir le nom du tournoi : '
        self.quest_place = 'Veuillez saisir le lieu du tournoi : '
        self.quest_desc = 'Veuillez saisir la description du tournoi : '
        self.quest_ctrl = 'Veuillez saisir le style de controle du temps : '
        self.quest_nb_round = 'Veuillez saisir le nombre de rounds : '

    def tournament_ask(self, quest) -> None:
        print(quest)
