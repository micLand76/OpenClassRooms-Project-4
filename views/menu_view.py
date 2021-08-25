class HomeMenuView:
    """ this class manage the display of the menu
    and the choice of the user """
    def __init__(self, menu):
        self.menu = menu

    def get_user_choice(self, menu_label):
        while True:
            """ display the menu to the user """
            self._display_menu(menu_label)
            """ ask to the user to make a choice """
            choice = input("> ")
            """ validate the user's choice """
            if choice in self.menu:
                return self.menu[choice]

    def _display_menu(self, menu_label):
        print(f"Menu {menu_label} : ")
        for key, entry in self.menu.items():
            print(f"{key}: {entry.option}")
