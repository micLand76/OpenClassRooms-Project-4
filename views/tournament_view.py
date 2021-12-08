class TournamentView:
    def __init__(self):
        """ questions to get the tournament's informations """
        self.quest_name = 'Veuillez saisir le nom du tournoi : '
        self.quest_place = 'Veuillez saisir le lieu du tournoi : '
        self.quest_desc = 'Veuillez saisir la description du tournoi : '
        self.quest_ctrl = 'Veuillez saisir le style de controle du temps (bullet, blitz ou coup rapide) : '
        self.quest_nb_round = 'Veuillez saisir le nombre de rounds : '

    @staticmethod
    def tournament_ask(quest: str) -> None:
        """ to display nicely the questions """
        print(quest)

    @staticmethod
    def display_message(message: str or None):
        print(message)

    @staticmethod
    def recept_message(demand: str or None):
        input(demand)
