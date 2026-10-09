import turtle
import time

import settings


class ArcadeTheme:
    """Unified arcade visual theme for all games"""
    
    # Core colors
    BG_DARK = "#0A0E27"
    BG_MEDIUM = "#1A1A3E"
    ACCENT_CYAN = "#00FF88"
    ACCENT_YELLOW = "#FFD700"
    ACCENT_MAGENTA = "#FF00FF"
    ACCENT_RED = "#FF1744"
    TEXT_PRIMARY = "#FFFFFF"
    TEXT_SECONDARY = "#B8C7CC"
    
    # Glow effects
    GLOW_CYAN = "#00FFAA"
    GLOW_MAGENTA = "#FF33FF"
    
    @staticmethod
    def draw_title_bar(screen, title, y_pos=280):
        """Draw an arcade-style title bar"""
        title_turtle = turtle.Turtle()
        title_turtle.hideturtle()
        title_turtle.penup()
        title_turtle.color(ArcadeTheme.ACCENT_CYAN)
        title_turtle.goto(0, y_pos)
        title_turtle.write(
            f"█ {title} █",
            align="center",
            font=("Courier", 32, "bold")
        )
        return title_turtle
    
    @staticmethod
    def draw_border(screen, x_min=-350, x_max=350, y_min=-260, y_max=260, color=None):
        """Draw an arcade-style border"""
        if color is None:
            color = ArcadeTheme.ACCENT_CYAN
        
        border = turtle.Turtle()
        border.hideturtle()
        border.speed(0)
        border.color(color)
        border.pensize(3)
        border.penup()
        border.goto(x_min, y_min)
        border.pendown()
        border.goto(x_max, y_min)
        border.goto(x_max, y_max)
        border.goto(x_min, y_max)
        border.goto(x_min, y_min)
        return border
    
    @staticmethod
    def draw_scanlines(screen):
        """Draw scanline effect for arcade feel"""
        scanlines = turtle.Turtle()
        scanlines.hideturtle()
        scanlines.speed(0)
        scanlines.color("#000000")
        scanlines.penup()
        
        for y in range(-260, 280, 4):
            scanlines.goto(-350, y)
            scanlines.pendown()
            scanlines.goto(350, y)
            scanlines.penup()


class SnakeGame:
    """Arcade-themed Snake Game"""
    
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("🐍 SNAKE - Arcade Edition")
        self.screen.bgcolor(ArcadeTheme.BG_DARK)
        self.screen.setup(width=800, height=700)
        self.screen.tracer(0)
        
        self.snake_list = []
        self.food_x = 0
        self.food_y = 0
        
        self.direction = "stop"
        self.score = 0
        self.running = False
        self.paused = False
        
        # UI
        self.score_turtle = turtle.Turtle()
        self.score_turtle.hideturtle()
        self.score_turtle.penup()
        self.score_turtle.color(ArcadeTheme.ACCENT_CYAN)
        self.score_turtle.goto(-320, 320)
        
        self.message_turtle = turtle.Turtle()
        self.message_turtle.hideturtle()
        self.message_turtle.penup()
        self.message_turtle.color(ArcadeTheme.TEXT_PRIMARY)
        
        self.setup_game()
    
    def setup_game(self):
        """Setup the game board"""
        ArcadeTheme.draw_border(self.screen)
        ArcadeTheme.draw_title_bar(self.screen, "SNAKE ARCADE")
        
        # Initial snake
        self.snake_list = []
        for i in range(3):
            segment = turtle.Turtle()
            segment.shape("square")
            segment.color(ArcadeTheme.ACCENT_CYAN if i == 0 else "#00CC66")
            segment.speed(0)
            segment.penup()
            segment.goto(-i * 20, 0)
            self.snake_list.append(segment)
        
        # Food
        self.spawn_food()
        self.draw_food()
        
        self.bind_controls()
    
    def spawn_food(self):
        """Spawn food at random location"""
        import random
        self.food_x = random.randint(-17, 17) * 20
        self.food_y = random.randint(-13, 13) * 20
    
    def draw_food(self):
        """Draw the food"""
        if not hasattr(self, 'food_turtle'):
            self.food_turtle = turtle.Turtle()
            self.food_turtle.shape("circle")
            self.food_turtle.color(ArcadeTheme.ACCENT_RED)
            self.food_turtle.speed(0)
            self.food_turtle.penup()
        self.food_turtle.goto(self.food_x, self.food_y)
    
    def bind_controls(self):
        """Bind keyboard controls"""
        self.screen.listen()
        self.screen.onkeypress(lambda: self.set_direction("up"), "Up")
        self.screen.onkeypress(lambda: self.set_direction("up"), "w")
        self.screen.onkeypress(lambda: self.set_direction("down"), "Down")
        self.screen.onkeypress(lambda: self.set_direction("down"), "s")
        self.screen.onkeypress(lambda: self.set_direction("left"), "Left")
        self.screen.onkeypress(lambda: self.set_direction("left"), "a")
        self.screen.onkeypress(lambda: self.set_direction("right"), "Right")
        self.screen.onkeypress(lambda: self.set_direction("right"), "d")
        self.screen.onkeypress(self.toggle_pause, "p")
        self.screen.onkeypress(self.return_to_menu, "m")
    
    def set_direction(self, direction):
        """Set snake direction"""
        opposites = {"up": "down", "down": "up", "left": "right", "right": "left"}
        if self.direction != opposites.get(direction):
            self.direction = direction
    
    def toggle_pause(self):
        """Toggle pause"""
        if not self.running:
            return
        self.paused = not self.paused
        if self.paused:
            self.message_turtle.goto(0, 0)
            self.message_turtle.write(
                "⏸ PAUSED ⏸\nPress P to continue | M for menu",
                align="center",
                font=("Arial", 20, "bold")
            )
        else:
            self.message_turtle.clear()
    
    def return_to_menu(self):
        """Return to main menu"""
        self.running = False
        self.screen.bye()
    
    def update_score_display(self):
        """Update score display"""
        self.score_turtle.clear()
        self.score_turtle.write(
            f"SCORE: {self.score}\nLENGTH: {len(self.snake_list)}",
            font=("Courier", 14, "bold")
        )
    
    def move_snake(self):
        """Move snake"""
        if not self.direction or self.direction == "stop":
            return
        
        head = self.snake_list[0]
        x, y = head.xcor(), head.ycor()
        
        if self.direction == "up":
            y += 20
        elif self.direction == "down":
            y -= 20
        elif self.direction == "left":
            x -= 20
        elif self.direction == "right":
            x += 20
        
        # Check collisions with walls
        if x < -340 or x > 340 or y < -250 or y > 250:
            self.game_over()
            return
        
        # Check collision with self
        for segment in self.snake_list:
            if segment.xcor() == x and segment.ycor() == y:
                self.game_over()
                return
        
        # Add new head
        new_head = turtle.Turtle()
        new_head.shape("square")
        new_head.color(ArcadeTheme.ACCENT_CYAN)
        new_head.speed(0)
        new_head.penup()
        new_head.goto(x, y)
        self.snake_list.insert(0, new_head)
        
        # Check food collision
        if x == self.food_x and y == self.food_y:
            self.score += 10
            self.spawn_food()
            self.draw_food()
        else:
            # Remove tail if no food eaten
            old_tail = self.snake_list.pop()
            old_tail.hideturtle()
        
        self.update_score_display()
    
    def game_over(self):
        """Game over"""
        self.running = False
        self.message_turtle.goto(0, 0)
        self.message_turtle.write(
            f"GAME OVER\nFinal Score: {self.score}\n\nPress M for menu",
            align="center",
            font=("Arial", 18, "bold")
        )
    
    def start_game(self):
        """Start the game"""
        self.running = True
        self.message_turtle.clear()
        self.game_loop()
    
    def game_loop(self):
        """Main game loop"""
        if self.running and not self.paused:
            self.move_snake()
        
        self.screen.update()
        
        if self.running:
            self.screen.ontimer(self.game_loop, 100)


class TetrisGame:
    """Arcade-themed Tetris Game"""
    
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("🟫 TETRIS - Arcade Edition")
        self.screen.bgcolor(ArcadeTheme.BG_DARK)
        self.screen.setup(width=700, height=800)
        self.screen.tracer(0)
        
        self.score = 0
        self.level = 1
        self.lines = 0
        self.running = False
        self.paused = False
        self.game_over_flag = False
        
        self.grid = [[0] * 10 for _ in range(20)]
        self.current_block = None
        self.fall_speed = 800
        self.last_fall = time.time()
        
        # UI
        self.score_turtle = turtle.Turtle()
        self.score_turtle.hideturtle()
        self.score_turtle.penup()
        self.score_turtle.color(ArcadeTheme.ACCENT_YELLOW)
        self.score_turtle.goto(-320, 320)
        
        self.message_turtle = turtle.Turtle()
        self.message_turtle.hideturtle()
        self.message_turtle.penup()
        self.message_turtle.color(ArcadeTheme.TEXT_PRIMARY)
        
        self.setup_game()
    
    def setup_game(self):
        """Setup the game board"""
        ArcadeTheme.draw_border(self.screen, -100, 100, -150, 250)
        ArcadeTheme.draw_title_bar(self.screen, "TETRIS ARCADE", 270)
        
        # Grid
        grid_pen = turtle.Turtle()
        grid_pen.hideturtle()
        grid_pen.speed(0)
        grid_pen.color("#333333")
        grid_pen.pensize(1)
        grid_pen.penup()
        
        for i in range(21):
            y = 250 - i * 20
            grid_pen.goto(-100, y)
            grid_pen.pendown()
            grid_pen.goto(100, y)
            grid_pen.penup()
        
        for i in range(11):
            x = -100 + i * 20
            grid_pen.goto(x, 250)
            grid_pen.pendown()
            grid_pen.goto(x, -150)
            grid_pen.penup()
        
        self.bind_controls()
    
    def bind_controls(self):
        """Bind keyboard controls"""
        self.screen.listen()
        self.screen.onkeypress(self.move_left, "Left")
        self.screen.onkeypress(self.move_left, "a")
        self.screen.onkeypress(self.move_right, "Right")
        self.screen.onkeypress(self.move_right, "d")
        self.screen.onkeypress(self.rotate, "Up")
        self.screen.onkeypress(self.rotate, "space")
        self.screen.onkeypress(self.toggle_pause, "p")
        self.screen.onkeypress(self.return_to_menu, "m")
    
    def move_left(self):
        pass
    
    def move_right(self):
        pass
    
    def rotate(self):
        pass
    
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
                font=("Arial", 20, "bold")
            )
        else:
            self.message_turtle.clear()
    
    def return_to_menu(self):
        """Return to main menu"""
        self.running = False
        self.screen.bye()
    
    def update_score_display(self):
        """Update score display"""
        self.score_turtle.clear()
        self.score_turtle.write(
            f"SCORE: {self.score}\nLEVEL: {self.level}\nLINES: {self.lines}",
            font=("Courier", 14, "bold")
        )
    
    def start_game(self):
        """Start the game"""
        self.running = True
        self.message_turtle.clear()
        self.message_turtle.goto(0, 0)
        self.message_turtle.write(
            "Simple Tetris Demo\n(Press M for menu)",
            align="center",
            font=("Arial", 16, "normal")
        )
    
    def game_loop(self):
        """Main game loop"""
        self.update_score_display()
        self.screen.update()
        
        if self.running:
            self.screen.ontimer(self.game_loop, 50)
