class PlayerView:
    def __init__(self):
        """ questions to get the player's informations """
        self.quest_name = 'Veuillez saisir le nom du joueur '
        self.quest_last_name = 'Veuillez saisir le prénom du joueur '
        self.quest_birth_date = 'Veuillez saisir la date de naissance du joueur '
        self.quest_sex = 'Veuillez saisir le sexe du joueur '

    @staticmethod
    def player_ask(quest, player) -> None:
        print(quest + f"{player} : ")

    @staticmethod
    def display_player():
        print("Joueur")
