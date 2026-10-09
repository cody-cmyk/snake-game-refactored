import random
import time
import turtle

import settings


class TetrisShape:
    """Represents a Tetris block with rotation and collision detection"""
    SHAPES = {
        'I': [(0, 0), (1, 0), (2, 0), (3, 0)],
        'O': [(0, 0), (1, 0), (0, 1), (1, 1)],
        'T': [(0, 0), (1, 0), (2, 0), (1, 1)],
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
    
    ROTATIONS = {
        'I': [
            [(0, 0), (1, 0), (2, 0), (3, 0)],
            [(0, 0), (0, 1), (0, 2), (0, 3)],
            [(0, 0), (1, 0), (2, 0), (3, 0)],
            [(0, 0), (0, 1), (0, 2), (0, 3)]
        ],
        'O': [
            [(0, 0), (1, 0), (0, 1), (1, 1)],
            [(0, 0), (1, 0), (0, 1), (1, 1)],
            [(0, 0), (1, 0), (0, 1), (1, 1)],
            [(0, 0), (1, 0), (0, 1), (1, 1)]
        ],
        'T': [
            [(0, 0), (1, 0), (2, 0), (1, 1)],
            [(0, 0), (0, 1), (1, 1), (0, 2)],
            [(1, 0), (0, 1), (1, 1), (2, 1)],
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
            [(0, 0), (1, 0), (0, 1), (0, 2)],
            [(0, 1), (1, 1), (2, 1), (2, 0)],
            [(0, 2), (0, 1), (0, 0), (1, 2)]
        ],
        'L': [
            [(2, 0), (0, 1), (1, 1), (2, 1)],
            [(0, 0), (0, 1), (0, 2), (1, 2)],
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
        """Returns list of (x, y) coordinates for current shape"""
        if self.shape_type in ['S', 'Z']:
            rotations = self.ROTATIONS[self.shape_type]
            shape = rotations[self.rotation_state % len(rotations)]
        else:
            rotations = self.ROTATIONS[self.shape_type]
            shape = rotations[self.rotation_state % len(rotations)]
        
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
        if self.shape_type in ['S', 'Z']:
            max_rotations = len(self.ROTATIONS[self.shape_type])
        else:
            max_rotations = len(self.ROTATIONS[self.shape_type])
        self.rotation_state = (self.rotation_state + 1) % max_rotations


class TetrisGame:
    """Main Tetris game class with full gameplay"""
    
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("TETRIS - Block Stack Challenge")
        self.screen.bgcolor("#1a1a1a")
        self.screen.setup(width=700, height=800)
        self.screen.tracer(0)
        
        self.grid_width = settings.TETRIS_GRID_WIDTH
        self.grid_height = settings.TETRIS_GRID_HEIGHT
        self.grid = [[0] * self.grid_width for _ in range(self.grid_height)]
        
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.running = True
        self.paused = False
        self.game_over_flag = False
        
        self.current_block = TetrisShape()
        self.fall_speed = 800
        self.last_fall_time = time.time()
        
        self.score_turtle = turtle.Turtle()
        self.score_turtle.hideturtle()
        self.score_turtle.penup()
        self.score_turtle.color("#00FF00")
        self.score_turtle.goto(-300, 320)
        
        self.message_turtle = turtle.Turtle()
        self.message_turtle.hideturtle()
        self.message_turtle.penup()
        self.message_turtle.color("#FFFFFF")
        
        self.next_block_turtle = turtle.Turtle()
        self.next_block_turtle.hideturtle()
        self.next_block_turtle.penup()
        self.next_block_turtle.color("#CCCCCC")
        self.next_block_turtle.goto(200, 200)
        
        self.draw_grid()
        self.bind_controls()
        self.update_display()
        self.game_loop()
    
    def draw_grid(self):
        """Draw the tetris playing field"""
        grid_turtle = turtle.Turtle()
        grid_turtle.hideturtle()
        grid_turtle.speed(0)
        grid_turtle.color("#333333")
        grid_turtle.pensize(1)
        grid_turtle.penup()
        
        # Draw horizontal lines
        for i in range(self.grid_height + 1):
            y = 250 - i * settings.TETRIS_BLOCK_SIZE
            grid_turtle.goto(-100, y)
            grid_turtle.pendown()
            grid_turtle.goto(100, y)
            grid_turtle.penup()
        
        # Draw vertical lines
        for i in range(self.grid_width + 1):
            x = -100 + i * settings.TETRIS_BLOCK_SIZE
            grid_turtle.goto(x, 250)
            grid_turtle.pendown()
            grid_turtle.goto(x, -150)
            grid_turtle.penup()
        
        # Draw border
        border_turtle = turtle.Turtle()
        border_turtle.hideturtle()
        border_turtle.speed(0)
        border_turtle.color("#00FF00")
        border_turtle.pensize(3)
        border_turtle.penup()
        border_turtle.goto(-100, 250)
        border_turtle.pendown()
        border_turtle.goto(100, 250)
        border_turtle.goto(100, -150)
        border_turtle.goto(-100, -150)
        border_turtle.goto(-100, 250)
    
    def bind_controls(self):
        """Bind keyboard controls"""
        self.screen.listen()
        self.screen.onkeypress(self.move_left, "Left")
        self.screen.onkeypress(self.move_right, "Right")
        self.screen.onkeypress(self.move_left, "a")
        self.screen.onkeypress(self.move_right, "d")
        self.screen.onkeypress(self.rotate, "space")
        self.screen.onkeypress(self.rotate, "Up")
        self.screen.onkeypress(self.hard_drop, "Down")
        self.screen.onkeypress(self.toggle_pause, "p")
        self.screen.onkeypress(self.quit_game, "q")
        self.screen.onkeypress(self.return_to_menu, "m")
    
    def move_left(self):
        """Move current block left"""
        if not self.game_over_flag and not self.paused:
            self.current_block.x -= 1
            if self.check_collision():
                self.current_block.x += 1
            self.current_block.draw(self.screen)
    
    def move_right(self):
        """Move current block right"""
        if not self.game_over_flag and not self.paused:
            self.current_block.x += 1
            if self.check_collision():
                self.current_block.x -= 1
            self.current_block.draw(self.screen)
    
    def rotate(self):
        """Rotate current block"""
        if not self.game_over_flag and not self.paused:
            self.current_block.rotate()
            if self.check_collision():
                self.current_block.rotation_state -= 1
            self.current_block.draw(self.screen)
    
    def hard_drop(self):
        """Drop block to bottom instantly"""
        if not self.game_over_flag and not self.paused:
            while not self.check_collision():
                self.current_block.y += 1
            self.current_block.y -= 1
            self.place_block()
    
    def check_collision(self):
        """Check if current block collides with grid or walls"""
        for x, y in self.current_block.get_blocks():
            if x < 0 or x >= self.grid_width or y >= self.grid_height:
                return True
            if y >= 0 and self.grid[y][x] != 0:
                return True
        return False
    
    def place_block(self):
        """Place current block on grid and spawn new one"""
        for x, y in self.current_block.get_blocks():
            if 0 <= y < self.grid_height and 0 <= x < self.grid_width:
                self.grid[y][x] = self.current_block.color
        
        self.current_block.clear_turtles()
        self.check_lines()
        self.spawn_block()
    
    def spawn_block(self):
        """Spawn a new block at the top"""
        self.current_block = TetrisShape()
        self.current_block.draw(self.screen)
        
        if self.check_collision():
            self.game_over_fn()
    
    def check_lines(self):
        """Check for completed lines and clear them"""
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
            self.draw_filled_blocks()
    
    def draw_filled_blocks(self):
        """Redraw all placed blocks on the grid"""
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
        """Update level based on lines cleared"""
        new_level = 1 + (self.lines_cleared // 10)
        if new_level > self.level:
            self.level = new_level
            self.fall_speed = max(200, 800 - (self.level * 50))
    
    def toggle_pause(self):
        """Toggle pause state"""
        if not self.game_over_flag:
            self.paused = not self.paused
            if self.paused:
                self.message_turtle.goto(0, 0)
                self.message_turtle.write("PAUSED\nPress P to continue", align="center", font=("Arial", 20, "bold"))
            else:
                self.message_turtle.clear()
    
    def game_over_fn(self):
        """Handle game over"""
        self.game_over_flag = True
        self.running = False
        self.message_turtle.goto(0, 0)
        self.message_turtle.write("GAME OVER!\nPress M for menu or Q to quit", align="center", font=("Arial", 18, "bold"))
    
    def return_to_menu(self):
        """Return to main menu"""
        self.running = False
        self.screen.bye()
    
    def quit_game(self):
        """Quit the game"""
        self.running = False
        self.screen.bye()
    
    def update_display(self):
        """Update score and level display"""
        self.score_turtle.clear()
        self.score_turtle.write(
            f"Score: {self.score}\nLevel: {self.level}\nLines: {self.lines_cleared}",
            font=("Arial", 16, "bold")
        )
        
        self.next_block_turtle.clear()
        self.next_block_turtle.write("NEXT", font=("Arial", 12, "bold"))
    
    def game_loop(self):
        """Main game loop"""
        if self.running and not self.paused and not self.game_over_flag:
            current_time = time.time()
            
            if (current_time - self.last_fall_time) * 1000 > self.fall_speed:
                self.current_block.y += 1
                self.last_fall_time = current_time
                
                if self.check_collision():
                    self.current_block.y -= 1
                    self.place_block()
                else:
                    self.current_block.draw(self.screen)
        
        self.update_display()
        self.screen.update()
        
        if self.running:
            self.screen.ontimer(self.game_loop, 50)
