from models.menu import Menu


class HomeMenuView:
    """ this class manage the display of the menu
    and the choice of the user """
    def __init__(self, menu: Menu):
        self.menu = menu

    def get_user_choice(self, menu_label: str) -> str:
        """ display the menu to the user,
        ask to the user to make a choice,
        and validate the user's choice"""
        while True:
            self._display_menu(menu_label)
            choice = input("> ")
            if choice in self.menu:
                return self.menu[choice]

    def _display_menu(self, menu_label: str):
        """ to display nicely the questions """
        print(f"Menu {menu_label} : ")
        for key, entry in self.menu.items():
            print(f"{key}: {entry.option}")
