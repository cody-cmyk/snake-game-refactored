import turtle
import random


class ArcadeTheme:
    """Arcade visual theme"""
    BG_DARK = "#0A0E27"
    ACCENT_CYAN = "#00FF88"
    ACCENT_RED = "#FF1744"
    ACCENT_YELLOW = "#FFD700"
    TEXT_PRIMARY = "#FFFFFF"


class SnakeGame:
    """Full-featured Snake game with arcade theme"""

    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("🐍 SNAKE - Arcade Edition")
        self.screen.bgcolor(ArcadeTheme.BG_DARK)
        self.screen.setup(width=900, height=700)
        self.screen.tracer(0)

        self.snake = []
        self.direction = "right"
        self.next_direction = "right"
        self.score = 0
        self.food_pos = (0, 0)
        self.running = True
        self.paused = False
        self.game_started = False

        self.setup_ui()
        self.show_start_screen()

    def setup_ui(self):
        """Setup UI elements"""
        # Score display
        self.score_turtle = turtle.Turtle()
        self.score_turtle.hideturtle()
        self.score_turtle.penup()
        self.score_turtle.color(ArcadeTheme.ACCENT_CYAN)
        self.score_turtle.goto(-380, 320)

        # Message display
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
        border.goto(-360, 280)
        border.pendown()
        border.goto(360, 280)
        border.goto(360, -280)
        border.goto(-360, -280)
        border.goto(-360, 280)

        # Title
        title = turtle.Turtle()
        title.hideturtle()
        title.penup()
        title.color(ArcadeTheme.ACCENT_CYAN)
        title.goto(0, 310)
        title.write("█ SNAKE ARCADE █", align="center", font=("Courier", 32, "bold"))

    def show_start_screen(self):
        """Show start screen"""
        self.message_turtle.goto(0, 50)
        self.message_turtle.write(
            "PRESS ENTER TO START\n\nArrow Keys or WASD to move\nP to pause | M for menu",
            align="center",
            font=("Courier", 16, "normal")
        )

        self.screen.listen()
        self.screen.onkeypress(self.start_game, "Return")
        self.screen.onkeypress(self.return_to_menu, "m")
        self.screen.update()

    def start_game(self):
        """Start the game"""
        self.game_started = True
        self.message_turtle.clear()
        self.init_snake()
        self.spawn_food()
        self.bind_controls()
        self.game_loop()

    def init_snake(self):
        """Initialize snake"""
        self.snake = []
        for i in range(3):
            segment = turtle.Turtle()
            segment.shape("square")
            segment.color(ArcadeTheme.ACCENT_CYAN if i == 0 else "#00AA66")
            segment.speed(0)
            segment.penup()
            segment.goto(-i * 20, 0)
            segment.shapesize(0.95, 0.95)
            self.snake.append(segment)

    def spawn_food(self):
        """Spawn food randomly"""
        x = random.randint(-17, 17) * 20
        y = random.randint(-13, 13) * 20
        self.food_pos = (x, y)

        if not hasattr(self, "food_turtle"):
            self.food_turtle = turtle.Turtle()
            self.food_turtle.shape("circle")
            self.food_turtle.color(ArcadeTheme.ACCENT_RED)
            self.food_turtle.speed(0)
            self.food_turtle.penup()
            self.food_turtle.shapesize(0.8, 0.8)

        self.food_turtle.goto(x, y)

    def bind_controls(self):
        """Bind keyboard controls"""
        self.screen.listen()
        self.screen.onkeypress(lambda: self.set_direction("up"), "Up")
        self.screen.onkeypress(lambda: self.set_direction("up"), "w")
        self.screen.onkeypress(lambda: self.set_direction("up"), "W")
        self.screen.onkeypress(lambda: self.set_direction("down"), "Down")
        self.screen.onkeypress(lambda: self.set_direction("down"), "s")
        self.screen.onkeypress(lambda: self.set_direction("down"), "S")
        self.screen.onkeypress(lambda: self.set_direction("left"), "Left")
        self.screen.onkeypress(lambda: self.set_direction("left"), "a")
        self.screen.onkeypress(lambda: self.set_direction("left"), "A")
        self.screen.onkeypress(lambda: self.set_direction("right"), "Right")
        self.screen.onkeypress(lambda: self.set_direction("right"), "d")
        self.screen.onkeypress(lambda: self.set_direction("right"), "D")
        self.screen.onkeypress(self.toggle_pause, "p")
        self.screen.onkeypress(self.toggle_pause, "P")
        self.screen.onkeypress(self.return_to_menu, "m")
        self.screen.onkeypress(self.return_to_menu, "M")

    def set_direction(self, direction):
        """Set snake direction"""
        opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
        if self.direction != opposites.get(direction):
            self.next_direction = direction

    def toggle_pause(self):
        """Toggle pause state"""
        if not self.game_started or not self.running:
            return
        self.paused = not self.paused
        if self.paused:
            self.message_turtle.goto(0, 0)
            self.message_turtle.write(
                "⏸ PAUSED ⏸\nPress P to continue | M for menu",
                align="center",
                font=("Courier", 18, "bold")
            )
        else:
            self.message_turtle.clear()

    def return_to_menu(self):
        """Return to main menu"""
        self.running = False
        self.screen.bye()

    def update_score(self):
        """Update score display"""
        self.score_turtle.clear()
        self.score_turtle.write(
            f"SCORE: {self.score} | LENGTH: {len(self.snake)}",
            font=("Courier", 14, "bold")
        )

    def move_snake(self):
        """Move snake in current direction"""
        self.direction = self.next_direction
        head = self.snake[0]
        x, y = head.xcor(), head.ycor()

        if self.direction == "up":
            y += 20
        elif self.direction == "down":
            y -= 20
        elif self.direction == "left":
            x -= 20
        elif self.direction == "right":
            x += 20

        # Check wall collision
        if x < -360 or x > 360 or y < -280 or y > 280:
            self.game_over("HIT THE WALL")
            return

        # Check self collision
        for segment in self.snake:
            if segment.xcor() == x and segment.ycor() == y:
                self.game_over("HIT YOURSELF")
                return

        # Add new head
        new_head = turtle.Turtle()
        new_head.shape("square")
        new_head.color(ArcadeTheme.ACCENT_CYAN)
        new_head.speed(0)
        new_head.penup()
        new_head.goto(x, y)
        new_head.shapesize(0.95, 0.95)
        self.snake.insert(0, new_head)

        # Check food collision
        if abs(x - self.food_pos[0]) < 15 and abs(y - self.food_pos[1]) < 15:
            self.score += 10
            self.spawn_food()
        else:
            # Remove tail
            tail = self.snake.pop()
            tail.hideturtle()

    def game_over(self, reason):
        """Handle game over"""
        self.running = False
        self.message_turtle.goto(0, 0)
        self.message_turtle.write(
            f"GAME OVER\n{reason}\nFinal Score: {self.score}\n\nPress M for menu",
            align="center",
            font=("Courier", 16, "bold")
        )

    def game_loop(self):
        """Main game loop"""
        if self.running and not self.paused:
            self.move_snake()

        self.update_score()
        self.screen.update()

        if self.running:
            self.screen.ontimer(self.game_loop, 100)
