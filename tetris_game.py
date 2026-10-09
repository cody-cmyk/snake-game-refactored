import turtle
import random
import time


class ArcadeTheme:
    """Arcade visual theme"""
    BG_DARK = "#0A0E27"
    ACCENT_CYAN = "#00FF88"
    ACCENT_YELLOW = "#FFD700"
    TEXT_PRIMARY = "#FFFFFF"


class TetrisShape:
    """Tetris piece"""

    SHAPES = {
        "I": [(0, 0), (1, 0), (2, 0), (3, 0)],
        "O": [(0, 0), (1, 0), (0, 1), (1, 1)],
        "T": [(1, 0), (0, 1), (1, 1), (2, 1)],
        "S": [(1, 0), (2, 0), (0, 1), (1, 1)],
        "Z": [(0, 0), (1, 0), (1, 1), (2, 1)],
        "J": [(0, 0), (0, 1), (1, 1), (2, 1)],
        "L": [(2, 0), (0, 1), (1, 1), (2, 1)],
    }

    COLORS = {
        "I": "#00FFFF",
        "O": "#FFFF00",
        "T": "#FF00FF",
        "S": "#00FF00",
        "Z": "#FF0000",
        "J": "#0000FF",
        "L": "#FFA500",
    }

    def __init__(self):
        self.shape_type = random.choice(list(self.SHAPES.keys()))
        self.color = self.COLORS[self.shape_type]
        self.x = 3
        self.y = 0
        self.turtles = []

    def get_blocks(self):
        shape = self.SHAPES[self.shape_type]
        return [(self.x + dx, self.y + dy) for dx, dy in shape]

    def draw(self, screen):
        self.clear()
        for x, y in self.get_blocks():
            t = turtle.Turtle()
            t.speed(0)
            t.shape("square")
            t.color(self.color)
            t.penup()
            screen_x = x * 20 - 100
            screen_y = 250 - y * 20
            t.goto(screen_x, screen_y)
            t.shapesize(1.9, 1.9)
            self.turtles.append(t)

    def clear(self):
        for t in self.turtles:
            t.hideturtle()
        self.turtles = []


class TetrisGame:
    """Full-featured Tetris game"""

    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("🟫 TETRIS - Arcade Edition")
        self.screen.bgcolor(ArcadeTheme.BG_DARK)
        self.screen.setup(width=700, height=800)
        self.screen.tracer(0)

        self.grid_width = 10
        self.grid_height = 20
        self.grid = [[0] * self.grid_width for _ in range(self.grid_height)]

        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.running = True
        self.paused = False
        self.game_over_flag = False

        self.current_block = TetrisShape()
        self.next_block = TetrisShape()
        self.fall_speed = 800
        self.last_fall = time.time()

        self.setup_ui()
        self.show_start_screen()

    def setup_ui(self):
        """Setup UI elements"""
        self.score_turtle = turtle.Turtle()
        self.score_turtle.hideturtle()
        self.score_turtle.penup()
        self.score_turtle.color(ArcadeTheme.ACCENT_YELLOW)
        self.score_turtle.goto(-300, 320)

        self.message_turtle = turtle.Turtle()
        self.message_turtle.hideturtle()
        self.message_turtle.penup()
        self.message_turtle.color(ArcadeTheme.TEXT_PRIMARY)

        # Draw border
        border = turtle.Turtle()
        border.hideturtle()
        border.speed(0)
        border.color(ArcadeTheme.ACCENT_CYAN)
        border.pensize(3)
        border.penup()
        border.goto(-100, 250)
        border.pendown()
        border.goto(100, 250)
        border.goto(100, -150)
        border.goto(-100, -150)
        border.goto(-100, 250)

        # Title
        title = turtle.Turtle()
        title.hideturtle()
        title.penup()
        title.color(ArcadeTheme.ACCENT_CYAN)
        title.goto(0, 280)
        title.write("█ TETRIS ARCADE █", align="center", font=("Courier", 28, "bold"))

        # Grid
        grid_pen = turtle.Turtle()
        grid_pen.hideturtle()
        grid_pen.speed(0)
        grid_pen.color("#333333")
        grid_pen.pensize(1)
        grid_pen.penup()

        for i in range(self.grid_height + 1):
            y = 250 - i * 20
            grid_pen.goto(-100, y)
            grid_pen.pendown()
            grid_pen.goto(100, y)
            grid_pen.penup()

        for i in range(self.grid_width + 1):
            x = -100 + i * 20
            grid_pen.goto(x, 250)
            grid_pen.pendown()
            grid_pen.goto(x, -150)
            grid_pen.penup()

    def show_start_screen(self):
        """Show start screen"""
        self.message_turtle.goto(0, 50)
        self.message_turtle.write(
            "PRESS ENTER TO START\n\nArrows/WASD to move\nSpace to rotate | M for menu",
            align="center",
            font=("Courier", 14, "normal")
        )

        self.screen.listen()
        self.screen.onkeypress(self.start_game, "Return")
        self.screen.onkeypress(self.return_to_menu, "m")
        self.screen.update()

    def start_game(self):
        """Start the game"""
        self.message_turtle.clear()
        self.current_block.draw(self.screen)
        self.bind_controls()
        self.game_loop()

    def bind_controls(self):
        """Bind keyboard controls"""
        self.screen.listen()
        self.screen.onkeypress(self.move_left, "Left")
        self.screen.onkeypress(self.move_left, "a")
        self.screen.onkeypress(self.move_left, "A")
        self.screen.onkeypress(self.move_right, "Right")
        self.screen.onkeypress(self.move_right, "d")
        self.screen.onkeypress(self.move_right, "D")
        self.screen.onkeypress(self.rotate_block, "Up")
        self.screen.onkeypress(self.rotate_block, "space")
        self.screen.onkeypress(self.hard_drop, "Down")
        self.screen.onkeypress(self.toggle_pause, "p")
        self.screen.onkeypress(self.toggle_pause, "P")
        self.screen.onkeypress(self.return_to_menu, "m")
        self.screen.onkeypress(self.return_to_menu, "M")

    def move_left(self):
        """Move block left"""
        if self.game_over_flag or self.paused:
            return
        self.current_block.x -= 1
        if self.check_collision():
            self.current_block.x += 1
        self.current_block.draw(self.screen)

    def move_right(self):
        """Move block right"""
        if self.game_over_flag or self.paused:
            return
        self.current_block.x += 1
        if self.check_collision():
            self.current_block.x -= 1
        self.current_block.draw(self.screen)

    def rotate_block(self):
        """Rotate block"""
        if self.game_over_flag or self.paused:
            return
        old_shape = self.current_block.shape_type
        self.current_block.shape_type = random.choice(list(TetrisShape.SHAPES.keys()))
        if self.check_collision():
            self.current_block.shape_type = old_shape
        self.current_block.draw(self.screen)

    def hard_drop(self):
        """Drop block to bottom"""
        if self.game_over_flag or self.paused:
            return
        while not self.check_collision():
            self.current_block.y += 1
        self.lock_block()

    def toggle_pause(self):
        """Toggle pause"""
        if self.game_over_flag:
            return
        self.paused = not self.paused
        if self.paused:
            self.message_turtle.goto(0, 0)
            self.message_turtle.write(
                "⏸ PAUSED ⏸\nPress P to continue | M for menu",
                align="center",
                font=("Courier", 16, "bold")
            )
        else:
            self.message_turtle.clear()

    def return_to_menu(self):
        """Return to main menu"""
        self.running = False
        self.screen.bye()

    def check_collision(self):
        """Check if block collides"""
        for x, y in self.current_block.get_blocks():
            if x < 0 or x >= self.grid_width or y >= self.grid_height:
                return True
            if y >= 0 and self.grid[y][x] != 0:
                return True
        return False

    def lock_block(self):
        """Lock block in place"""
        for x, y in self.current_block.get_blocks():
            if 0 <= y < self.grid_height and 0 <= x < self.grid_width:
                self.grid[y][x] = self.current_block.color

        self.current_block.clear()
        self.clear_lines()
        self.current_block = self.next_block
        self.next_block = TetrisShape()

        if self.check_collision():
            self.game_over_fn()
        else:
            self.current_block.draw(self.screen)

    def clear_lines(self):
        """Clear completed lines"""
        lines_to_clear = []
        for y in range(self.grid_height):
            if all(self.grid[y][x] != 0 for x in range(self.grid_width)):
                lines_to_clear.append(y)

        if lines_to_clear:
            for y in sorted(lines_to_clear, reverse=True):
                del self.grid[y]
                self.grid.insert(0, [0] * self.grid_width)

            self.lines_cleared += len(lines_to_clear)
            self.score += 100 * (len(lines_to_clear) ** 2) * self.level
            self.level = 1 + (self.lines_cleared // 10)
            self.fall_speed = max(200, 800 - (self.level * 40))

    def update_display(self):
        """Update score display"""
        self.score_turtle.clear()
        self.score_turtle.write(
            f"SCORE: {self.score}\nLEVEL: {self.level}\nLINES: {self.lines_cleared}",
            font=("Courier", 12, "bold")
        )

    def game_over_fn(self):
        """Game over"""
        self.game_over_flag = True
        self.running = False
        self.message_turtle.goto(0, 0)
        self.message_turtle.write(
            f"GAME OVER\nFinal Score: {self.score}\nLevel: {self.level}\n\nPress M for menu",
            align="center",
            font=("Courier", 14, "bold")
        )

    def game_loop(self):
        """Main game loop"""
        if self.running and not self.paused and not self.game_over_flag:
            current_time = time.time()
            if (current_time - self.last_fall) * 1000 > self.fall_speed:
                self.current_block.y += 1
                self.last_fall = current_time

                if self.check_collision():
                    self.current_block.y -= 1
                    self.lock_block()
                else:
                    self.current_block.draw(self.screen)

        self.update_display()
        self.screen.update()

        if self.running:
            self.screen.ontimer(self.game_loop, 50)
