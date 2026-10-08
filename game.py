import settings


class ControlBinder:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game

    def bind(self):
        self.screen.listen()

        for key in settings.UP_KEYS:
            self.screen.onkeypress(lambda key=key: self.game.set_direction("up"), key)

        for key in settings.DOWN_KEYS:
            self.screen.onkeypress(lambda key=key: self.game.set_direction("down"), key)

        for key in settings.LEFT_KEYS:
            self.screen.onkeypress(lambda key=key: self.game.set_direction("left"), key)

        for key in settings.RIGHT_KEYS:
            self.screen.onkeypress(lambda key=key: self.game.set_direction("right"), key)

        self.screen.onkeypress(self.game.toggle_pause, "p")
        self.screen.onkeypress(self.game.restart_game, "r")
        self.screen.onkeypress(self.game.quit_game, "q")

        self.screen.onkeypress(self.game.show_admin_panel, "a")
        self.screen.onkeypress(self.game.show_main_menu, "m")
