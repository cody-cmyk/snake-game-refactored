import random
import time
import turtle

import settings


class TetrisShape:
    """Represents a falling Tetris piece with rotation support"""
    
    SHAPES = {
        'I': [(0, 0), (1, 0), (2, 0), (3, 0)],
        'O': [(0, 0), (1, 0), (0, 1), (1, 1)],
        'T': [(1, 0), (0, 1), (1, 1), (2, 1)],
        'S': [(1, 0), (2, 0), (0, 1), (1, 1)],
        'Z': [(0, 0), (1, 0), (1, 1), (2, 1)],
        'J': [(0, 0), (0, 1), (1, 1), (2, 1)],
        'L': [(2, 0), (0, 1), (1, 1), (2, 1)]
    }
    
    COLORS = {
        'I': '#00FFFF',
        'O': '#FFFF00',
        'T': '#FF00FF',
        'S': '#00FF00',
        'Z': '#FF0000',
        'J': '#0000FF',
        'L': '#FFA500'
    }
    
    # Rotation states for each piece
    ROTATIONS = {
        'I': [
            [(0, 0), (1, 0), (2, 0), (3, 0)],
            [(0, 0), (0, 1), (0, 2), (0, 3)],
            [(0, 0), (1, 0), (2, 0), (3, 0)],
            [(0, 0), (0, 1), (0, 2), (0, 3)]
        ],
        'O': [[(0, 0), (1, 0), (0, 1), (1, 1)]] * 4,
        'T': [
            [(1, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (0, 1), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (1, 2)],
            [(1, 0), (0, 1), (1, 1), (1, 2)]
        ],
        'S': [
            [(1, 0), (2, 0), (0, 1), (1, 1)],
            [(0, 0), (0, 1), (1, 1), (1, 2)]
        ],
        'Z': [
            [(0, 0), (1, 0), (1, 1), (2, 1)],
            [(1, 0), (0, 1), (1, 1), (0, 2)]
        ],
        'J': [
            [(0, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (1, 1), (0, 2), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (2, 0)],
            [(0, 0), (0, 1), (1, 1), (1, 2)]
        ],
        'L': [
            [(2, 0), (0, 1), (1, 1), (2, 1)],
            [(0, 0), (0, 1), (1, 1), (1, 2)],
            [(0, 0), (1, 0), (2, 0), (0, 1)],
            [(0, 0), (1, 0), (1, 1), (1, 2)]
        ]
    }
    
    def __init__(self, shape_type=None):
        self.shape_type = shape_type or random.choice(list(self.SHAPES.keys()))
        self.color = self.COLORS[self.shape_type]
        self.x = 3
        self.y = 0
        self.rotation_state = 0
        self.turtles = []
    
    def get_blocks(self):
        """Get current block positions based on rotation state"""
        rotations = self.ROTATIONS[self.shape_type]
        rotation_index = self.rotation_state % len(rotations)
        shape = rotations[rotation_index]
        return [(self.x + dx, self.y + dy) for dx, dy in shape]
    
    def draw(self, screen):
        """Draw the shape on screen"""
        self.clear_turtles()
        
        for x, y in self.get_blocks():
            t = turtle.Turtle()
            t.speed(0)
            t.shape("square")
            t.color(self.color)
            t.penup()
            screen_x = x * settings.TETRIS_BLOCK_SIZE - 100
            screen_y = 250 - y * settings.TETRIS_BLOCK_SIZE
            t.goto(screen_x, screen_y)
            t.shapesize(1.9, 1.9)
            self.turtles.append(t)
    
    def clear_turtles(self):
        """Hide and clear all turtles"""
        for t in self.turtles:
            t.hideturtle()
        self.turtles.clear()
    
    def rotate(self):
        """Rotate the shape"""
        rotations = self.ROTATIONS[self.shape_type]
        self.rotation_state = (self.rotation_state + 1) % len(rotations)
    
    def move_left(self):
        self.x -= 1
    
    def move_right(self):
        self.x += 1
    
    def move_down(self):
        self.y += 1


class TetrisGame:
    """Full-featured Tetris game with collision, line clearing, and scoring"""
    
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("🎮 TETRIS - Block Stack Challenge 🎮")
        self.screen.bgcolor("#1a1a2e")
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
        
        # UI elements
        self.score_turtle = turtle.Turtle()
        self.score_turtle.hideturtle()
        self.score_turtle.penup()
        self.score_turtle.color("#00FF00")
        self.score_turtle.goto(-320, 320)
        
        self.next_turtle = turtle.Turtle()
        self.next_turtle.hideturtle()
        self.next_turtle.penup()
        self.next_turtle.color("#FFFF00")
        self.next_turtle.goto(180, 280)
        
        self.message_turtle = turtle.Turtle()
        self.message_turtle.hideturtle()
        self.message_turtle.penup()
        self.message_turtle.color("#FFFFFF")
        
        self.draw_ui()
        self.bind_controls()
        self.current_block.draw(self.screen)
        self.game_loop()
    
    def draw_ui(self):
        """Draw game borders and UI elements"""
        border = turtle.Turtle()
        border.hideturtle()
        border.speed(0)
        border.color("#00FF00")
        border.pensize(3)
        border.penup()
        border.goto(-100, 250)
        border.pendown()
        border.goto(100, 250)
        border.goto(100, -150)
        border.goto(-100, -150)
        border.goto(-100, 250)
        
        # Grid lines
        grid_pen = turtle.Turtle()
        grid_pen.hideturtle()
        grid_pen.speed(0)
        grid_pen.color("#333333")
        grid_pen.pensize(1)
        grid_pen.penup()
        
        for i in range(self.grid_height + 1):
            y = 250 - i * settings.TETRIS_BLOCK_SIZE
            grid_pen.goto(-100, y)
            grid_pen.pendown()
            grid_pen.goto(100, y)
            grid_pen.penup()
        
        for i in range(self.grid_width + 1):
            x = -100 + i * settings.TETRIS_BLOCK_SIZE
            grid_pen.goto(x, 250)
            grid_pen.pendown()
            grid_pen.goto(x, -150)
            grid_pen.penup()
        
        # Title
        title = turtle.Turtle()
        title.hideturtle()
        title.penup()
        title.color("#00FF00")
        title.goto(0, 280)
        title.write("TETRIS", align="center", font=("Arial", 24, "bold"))
        
        # Instructions
        instructions = turtle.Turtle()
        instructions.hideturtle()
        instructions.penup()
        instructions.color("#CCCCCC")
        instructions.goto(0, -200)
        instructions.write(
            "◄ ► or A/D: Move | ↑ or Space: Rotate | P: Pause | Q: Quit | M: Menu",
            align="center",
            font=("Arial", 10, "normal")
        )
    
    def update_display(self):
        """Update score and level display"""
        self.score_turtle.clear()
        self.score_turtle.write(
            f"SCORE: {self.score}\nLEVEL: {self.level}\nLINES: {self.lines_cleared}",
            font=("Arial", 16, "bold")
        )
        
        self.next_turtle.clear()
        self.next_turtle.write("NEXT", font=("Arial", 14, "bold"))
    
    def bind_controls(self):
        """Bind keyboard controls"""
        self.screen.listen()
        self.screen.onkeypress(self.move_left, "Left")
        self.screen.onkeypress(self.move_left, "a")
        self.screen.onkeypress(self.move_left, "A")
        self.screen.onkeypress(self.move_right, "Right")
        self.screen.onkeypress(self.move_right, "d")
        self.screen.onkeypress(self.move_right, "D")
        self.screen.onkeypress(self.rotate, "Up")
        self.screen.onkeypress(self.rotate, "space")
        self.screen.onkeypress(self.hard_drop, "Down")
        self.screen.onkeypress(self.toggle_pause, "p")
        self.screen.onkeypress(self.toggle_pause, "P")
        self.screen.onkeypress(self.quit_game, "q")
        self.screen.onkeypress(self.quit_game, "Q")
        self.screen.onkeypress(self.return_to_menu, "m")
        self.screen.onkeypress(self.return_to_menu, "M")
    
    def move_left(self):
        """Move block left with collision check"""
        if self.game_over_flag or self.paused:
            return
        self.current_block.move_left()
        if self.check_collision():
            self.current_block.move_right()
        self.current_block.draw(self.screen)
    
    def move_right(self):
        """Move block right with collision check"""
        if self.game_over_flag or self.paused:
            return
        self.current_block.move_right()
        if self.check_collision():
            self.current_block.move_left()
        self.current_block.draw(self.screen)
    
    def rotate(self):
        """Rotate block with collision check"""
        if self.game_over_flag or self.paused:
            return
        self.current_block.rotate()
        if self.check_collision():
            # Rotate back if collision
            self.current_block.rotation_state -= 1
        self.current_block.draw(self.screen)
    
    def hard_drop(self):
        """Drop block to bottom instantly"""
        if self.game_over_flag or self.paused:
            return
        while not self.check_collision():
            self.current_block.move_down()
        self.current_block.move_down()  # Go one down past the collision
        self.lock_block()
    
    def toggle_pause(self):
        """Toggle pause state"""
        if self.game_over_flag:
            return
        self.paused = not self.paused
        if self.paused:
            self.message_turtle.goto(0, 0)
            self.message_turtle.write(
                "⏸ PAUSED ⏸\nPress P to continue",
                align="center",
                font=("Arial", 28, "bold")
            )
        else:
            self.message_turtle.clear()
    
    def return_to_menu(self):
        """Return to main menu"""
        self.running = False
        self.screen.bye()
    
    def quit_game(self):
        """Quit the game"""
        self.running = False
        self.screen.bye()
    
    def check_collision(self):
        """Check if current block collides with walls or placed blocks"""
        for x, y in self.current_block.get_blocks():
            if x < 0 or x >= self.grid_width or y >= self.grid_height:
                return True
            if y >= 0 and self.grid[y][x] != 0:
                return True
        return False
    
    def lock_block(self):
        """Lock current block in place and spawn new one"""
        for x, y in self.current_block.get_blocks():
            if 0 <= y < self.grid_height and 0 <= x < self.grid_width:
                self.grid[y][x] = self.current_block.color
        
        self.current_block.clear_turtles()
        self.clear_lines()
        
        self.current_block = self.next_block
        self.next_block = TetrisShape()
        
        if self.check_collision():
            self.game_over_fn()
        else:
            self.current_block.draw(self.screen)
    
    def clear_lines(self):
        """Clear completed lines and award points"""
        lines_to_clear = []
        
        for y in range(self.grid_height):
            if all(self.grid[y][x] != 0 for x in range(self.grid_width)):
                lines_to_clear.append(y)
        
        if lines_to_clear:
            for y in sorted(lines_to_clear, reverse=True):
                del self.grid[y]
                self.grid.insert(0, [0] * self.grid_width)
            
            lines_cleared = len(lines_to_clear)
            self.lines_cleared += lines_cleared
            
            # Scoring: 100 * lines^2 * level
            points = int(100 * (lines_cleared ** 2) * self.level)
            self.score += points
            
            self.update_level()
            self.redraw_grid()
    
    def redraw_grid(self):
        """Redraw all placed blocks"""
        # Clear old blocks
        for turtle_obj in turtle.turtles():
            if turtle_obj not in [self.score_turtle, self.next_turtle, self.message_turtle]:
                if hasattr(turtle_obj, 'shape') and turtle_obj.shape() == "square":
                    turtle_obj.hideturtle()
        
        # Draw grid blocks
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if self.grid[y][x] != 0:
                    t = turtle.Turtle()
                    t.speed(0)
                    t.shape("square")
                    t.color(self.grid[y][x])
                    t.penup()
                    screen_x = x * settings.TETRIS_BLOCK_SIZE - 100
                    screen_y = 250 - y * settings.TETRIS_BLOCK_SIZE
                    t.goto(screen_x, screen_y)
                    t.shapesize(1.9, 1.9)
    
    def update_level(self):
        """Update level and fall speed based on lines cleared"""
        new_level = 1 + (self.lines_cleared // 10)
        if new_level > self.level:
            self.level = new_level
            self.fall_speed = max(200, 800 - (self.level * 40))
    
    def game_over_fn(self):
        """Handle game over state"""
        self.game_over_flag = True
        self.running = False
        self.message_turtle.goto(0, 0)
        self.message_turtle.write(
            f"GAME OVER!\nFinal Score: {self.score}\nLevel: {self.level}\n\nPress M for menu or Q to quit",
            align="center",
            font=("Arial", 20, "bold")
        )
    
    def game_loop(self):
        """Main game loop"""
        if self.running and not self.paused and not self.game_over_flag:
            current_time = time.time()
            
            if (current_time - self.last_fall) * 1000 > self.fall_speed:
                self.current_block.move_down()
                self.last_fall = current_time
                
                if self.check_collision():
                    self.current_block.move_down()  # Go back up
                    self.lock_block()
                else:
                    self.current_block.draw(self.screen)
        
        self.update_display()
        self.screen.update()
        
        if self.running:
            self.screen.ontimer(self.game_loop, 50)
