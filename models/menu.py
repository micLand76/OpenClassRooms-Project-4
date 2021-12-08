from collections.abc import ItemsView


class Menu:
    """ this class contains methods to manage the menu
    the attribut _entries contains the dictionary of the menu option
    and _autokey contains the key of the menu: we don't need to give a number
    to each menu, the 'auto' value will give the value with the autokey attribut
    """
    def __init__(self):
        self._entries = {}
        self._autokey = 1

    def add(self, key: str, option: str, handler):
        """ it allows to add menu options """
        if key == "auto":
            key = str(self._autokey)
            self._autokey += 1
        self._entries[str(key)] = MenuEntry(option, handler)

    def clear(self):
        """ when we display a new menu, we clear the old menu """
        self._entries = {}
        self._autokey = 1

    def items(self) -> ItemsView:
        """ iterator of the entries """
        return self._entries.items()

    def __getitem__(self, choice: str) -> str:
        return self._entries[choice]

    def __contains__(self, choice: str) -> bool:
        return str(choice) in self._entries


class MenuEntry:
    """ this class is used to associate an option menu with a handler
    to manage the functions of the menu chosen """
    def __init__(self, option: str, handler):
        self.option = option
        self.handler = handler

    def __str__(self) -> str:
        return str(self.option)
