from controllers.menu_management import HomeMenuController


class Controller:
    """ Main controller """
    def __init__(self):
        self.controller = None

    def start(self):
        """ at the beginning of the app, we start with the menu
        which is called in the HomeMenuController """
        self.controller = HomeMenuController()
        while self.controller:
            self.controller = self.controller()
