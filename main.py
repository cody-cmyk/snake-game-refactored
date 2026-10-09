import turtle

from menu import Menu
from snake_game import SnakeGame
from tetris import TetrisGame
from admin import AdminController
import settings


class ArcadeLauncher:
    """Shared launcher that lets you choose Snake or Tetris from the same menu."""

    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("ARCADE GAMES")
        self.screen.bgcolor("#0a0a0a")
        self.screen.setup(width=settings.WINDOW_WIDTH, height=settings.WINDOW_HEIGHT)
        self.screen.tracer(0)

        self.admin_controller = AdminController()
        self.menu = Menu(self.screen)
        self.show_main_menu()

    def reset_screen(self):
        self.screen = turtle.Screen()
        self.screen.title("ARCADE GAMES")
        self.screen.bgcolor("#0a0a0a")
        self.screen.setup(width=settings.WINDOW_WIDTH, height=settings.WINDOW_HEIGHT)
        self.screen.tracer(0)
        self.menu = Menu(self.screen)

    def show_main_menu(self):
        callbacks = {
            "snake": self.launch_snake,
            "tetris": self.launch_tetris,
            "settings": self.show_settings_menu,
            "quit": self.quit_game,
        }
        self.menu.show_main_menu(callbacks)
        self.screen.update()

    def launch_snake(self):
        self.menu.clear_screen()
        self.screen.bye()

        game = SnakeGame()
        game.screen.mainloop()

        self.reset_screen()
        self.show_main_menu()

    def launch_tetris(self):
        self.menu.clear_screen()
        self.screen.bye()

        game = TetrisGame()
        game.screen.mainloop()

        self.reset_screen()
        self.show_main_menu()

    def show_settings_menu(self):
        self.admin_controller.admin_mode = True
        callbacks = {
            "adjust_points": self.show_adjust_points_menu,
            "adjust_speed": self.show_adjust_speed_menu,
            "adjust_animation": self.show_adjust_animation_menu,
            "back": self.show_main_menu,
        }
        self.menu.show_settings_menu(self.admin_controller, callbacks)
        self.screen.update()

    def show_adjust_points_menu(self):
        def increase_points():
            self.admin_controller.adjust_points(10)
            self.show_adjust_points_menu()

        def decrease_points():
            self.admin_controller.adjust_points(-10)
            self.show_adjust_points_menu()

        callbacks = {
            "increase": increase_points,
            "decrease": decrease_points,
            "confirm": self.show_settings_menu,
            "cancel": self.show_settings_menu,
        }
        self.menu.show_adjust_points_menu(
            self.admin_controller.admin_points_per_food,
            callbacks,
        )
        self.screen.update()

    def show_adjust_speed_menu(self):
        def increase_speed():
            self.admin_controller.adjust_speed(0.1)
            self.show_adjust_speed_menu()

        def decrease_speed():
            self.admin_controller.adjust_speed(-0.1)
            self.show_adjust_speed_menu()

        callbacks = {
            "increase": increase_speed,
            "decrease": decrease_speed,
            "confirm": self.show_settings_menu,
            "cancel": self.show_settings_menu,
        }
        self.menu.show_adjust_speed_menu(
            self.admin_controller.admin_speed_multiplier,
            callbacks,
        )
        self.screen.update()

    def show_adjust_animation_menu(self):
        callbacks = {
            "set_animation": self.set_animation_level,
            "back": self.show_settings_menu,
        }
        self.menu.show_adjust_animation_menu(
            self.admin_controller.admin_animation_level,
            callbacks,
        )
        self.screen.update()

    def set_animation_level(self, level):
        self.admin_controller.set_animation(level)
        self.show_adjust_animation_menu()

    def quit_game(self):
        self.screen.bye()
        raise SystemExit


def main():
    launcher = ArcadeLauncher()
    launcher.screen.mainloop()


if __name__ == "__main__":
    main()
