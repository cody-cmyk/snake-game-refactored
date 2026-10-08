import random
import time
import turtle

import settings


class TetrisBlock:
    def __init__(self, shape_type, screen):
        self.shape_type = shape_type
        self.screen = screen
        self.turtles = []
        self.x = settings.TETRIS_SPAWN_X
        self.y = settings.TETRIS_SPAWN_Y
        self.shape = settings.TETRIS_SHAPES[shape_type]
        self.color = settings.TETRIS_COLORS[shape_type]
        self.rotation = 0
        self.draw()

    def draw(self):
        for turtle_obj in self.turtles:
            turtle_obj.hideturtle()
        self.turtles.clear()

        for (dx, dy) in self.shape:
            block = turtle.Turtle()
            block.speed(0)
            block.shape("square")
            block.color(self.color)
            block.penup()
            px = (self.x + dx) * settings.TETRIS_BLOCK_SIZE - 100
            py = 250 - (self.y + dy) * settings.TETRIS_BLOCK_SIZE
            block.goto(px, py)
            block.shapesize(1.9, 1.9)
            self.turtles.append(block)

    def move_down(self):
        self.y += 1
        self.draw()

    def move_left(self):
        if self.x > 0:
            self.x -= 1
            self.draw()

    def move_right(self):
        if self.x < settings.TETRIS_GRID_WIDTH - 3:
            self.x += 1
            self.draw()

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4
        self.draw()

    def clear(self):
        for t in self.turtles:
            t.hideturtle()
        self.turtles.clear()


class TetrisGame:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("TETRIS")
        self.screen.bgcolor(settings.TETRIS_BACKGROUND)
        self.screen.setup(width=600, height=700)
        self.screen.tracer(0)

        self.score = 0
        self.level = 1
        self.running = True
        self.paused = False
        self.grid = [[0] * settings.TETRIS_GRID_WIDTH for _ in range(settings.TETRIS_GRID_HEIGHT)]
        self.current_block = None
        self.fall_speed = 1000

        self.score_writer = turtle.Turtle()
        self.score_writer.hideturtle()
        self.score_writer.penup()
        self.score_writer.color("#FFFFFF")
        self.score_writer.goto(-250, 300)

        self.message_writer = turtle.Turtle()
        self.message_writer.hideturtle()
        self.message_writer.penup()
        self.message_writer.color("#FFFFFF")

        self.draw_grid()
        self.bind_controls()
        self.spawn_block()
        self.game_loop()

    def draw_grid(self):
        grid_drawer = turtle.Turtle()
        grid_drawer.hideturtle()
        grid_drawer.speed(0)
        grid_drawer.color("#333333")
        grid_drawer.penup()

        for i in range(settings.TETRIS_GRID_HEIGHT + 1):
            grid_drawer.goto(-100, 250 - i * settings.TETRIS_BLOCK_SIZE)
            grid_drawer.pendown()
            grid_drawer.goto(100, 250 - i * settings.TETRIS_BLOCK_SIZE)
            grid_drawer.penup()

        for i in range(settings.TETRIS_GRID_WIDTH + 1):
            grid_drawer.goto(-100 + i * settings.TETRIS_BLOCK_SIZE, 250)
            grid_drawer.pendown()
            grid_drawer.goto(-100 + i * settings.TETRIS_BLOCK_SIZE, -150)
            grid_drawer.penup()

    def spawn_block(self):
        shape = random.choice(list(settings.TETRIS_SHAPES.keys()))
        self.current_block = TetrisBlock(shape, self.screen)

    def update_score_display(self):
        self.score_writer.clear()
        self.score_writer.write(
            f"Score: {self.score}\nLevel: {self.level}",
            font=("Arial", 16, "bold")
        )

    def bind_controls(self):
        self.screen.listen()
        self.screen.onkeypress(self.current_block.move_left, "Left")
        self.screen.onkeypress(self.current_block.move_right, "Right")
        self.screen.onkeypress(self.current_block.rotate, "space")
        self.screen.onkeypress(self.toggle_pause, "p")
        self.screen.onkeypress(self.quit_game, "q")

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.message_writer.goto(0, 0)
            self.message_writer.write("PAUSED\nPress P to continue", align="center", font=("Arial", 24, "bold"))
        else:
            self.message_writer.clear()

    def quit_game(self):
        self.running = False
        self.screen.bye()

    def game_loop(self):
        if self.running and not self.paused:
            self.current_block.move_down()

            if self.current_block.y >= settings.TETRIS_GRID_HEIGHT - 2:
                self.spawn_block()
                self.score += 10
                self.level = max(1, self.score // 100)
                self.fall_speed = max(200, 1000 - (self.level * 50))

        self.update_score_display()
        self.screen.update()

        if self.running:
            self.screen.ontimer(self.game_loop, self.fall_speed)
