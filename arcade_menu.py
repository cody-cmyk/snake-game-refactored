import turtle
from snake_game import SnakeGame
from tetris_game import TetrisGame


class ArcadeTheme:
    """Unified arcade visual theme"""
    BG_DARK = "#0A0E27"
    BG_MEDIUM = "#1A1A3E"
    ACCENT_CYAN = "#00FF88"
    ACCENT_YELLOW = "#FFD700"
    ACCENT_MAGENTA = "#FF00FF"
    ACCENT_RED = "#FF1744"
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#B8C7CC"


class ArcadeMenu:
    """Main arcade game menu"""

    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("🎮 ARCADE GAMES 🎮")
        self.screen.bgcolor(ArcadeTheme.BG_DARK)
        self.screen.setup(width=900, height=700)
        self.screen.tracer(0)

        self.current_menu = "main"
        self.setup_fonts()
        self.show_main_menu()

    def setup_fonts(self):
        """Register custom fonts"""
        pass

    def clear_all_turtles(self):
        """Clear all turtles from screen"""
        for turtle_obj in turtle.turtles():
            turtle_obj.hideturtle()

    def draw_menu_box(self, y_pos, width=500, height=300):
        """Draw a decorative menu box"""
        box = turtle.Turtle()
        box.hideturtle()
        box.speed(0)
        box.color(ArcadeTheme.ACCENT_CYAN)
        box.pensize(3)
        box.penup()
        box.goto(-width // 2, y_pos + height // 2)
        box.pendown()
        box.goto(width // 2, y_pos + height // 2)
        box.goto(width // 2, y_pos - height // 2)
        box.goto(-width // 2, y_pos - height // 2)
        box.goto(-width // 2, y_pos + height // 2)

    def draw_title(self, title, y_pos=300):
        """Draw arcade-style title"""
        title_turtle = turtle.Turtle()
        title_turtle.hideturtle()
        title_turtle.penup()
        title_turtle.color(ArcadeTheme.ACCENT_CYAN)
        title_turtle.goto(0, y_pos)
        title_turtle.write(
            f"█ {title} █",
            align="center",
            font=("Courier", 48, "bold")
        )
        return title_turtle

    def show_main_menu(self):
        """Display main menu"""
        self.clear_all_turtles()
        self.current_menu = "main"

        # Title
        self.draw_title("ARCADE GAMES", 280)

        # Menu box
        self.draw_menu_box(0, 600, 350)

        # Options
        options = turtle.Turtle()
        options.hideturtle()
        options.penup()
        options.color(ArcadeTheme.TEXT_PRIMARY)
        options.goto(0, 100)
        options.write(
            "1  ▶  SNAKE  ◀",
            align="center",
            font=("Courier", 28, "bold")
        )

        options.goto(0, 20)
        options.write(
            "2  ▶  TETRIS  ◀",
            align="center",
            font=("Courier", 28, "bold")
        )

        options.goto(0, -60)
        options.write(
            "3  ▶  QUIT  ◀",
            align="center",
            font=("Courier", 28, "bold")
        )

        # Instructions
        instructions = turtle.Turtle()
        instructions.hideturtle()
        instructions.penup()
        instructions.color(ArcadeTheme.TEXT_SECONDARY)
        instructions.goto(0, -250)
        instructions.write(
            "Press 1, 2, or 3 to select",
            align="center",
            font=("Courier", 14, "normal")
        )

        self.screen.listen()
        self.screen.onkeypress(self.launch_snake, "1")
        self.screen.onkeypress(self.launch_tetris, "2")
        self.screen.onkeypress(self.quit_app, "3")
        self.screen.update()

    def launch_snake(self):
        """Launch Snake game"""
        self.screen.bye()
        game = SnakeGame()
        game.screen.mainloop()
        self.reinit_menu()

    def launch_tetris(self):
        """Launch Tetris game"""
        self.screen.bye()
        game = TetrisGame()
        game.screen.mainloop()
        self.reinit_menu()

    def reinit_menu(self):
        """Reinitialize menu after game closes"""
        self.__init__()

    def quit_app(self):
        """Quit the application"""
        self.screen.bye()
