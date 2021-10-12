from controllers.menu_management import HomeMenuController


class Controller:
    """ Main controller """
    def __init__(self):
        self.controller = None

    def start(self):
        self.controller = HomeMenuController()
        while self.controller:
            self.controller = self.controller()
