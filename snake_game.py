import random
import time
import turtle

import settings
from admin import AdminController
from animations import AnimationManager
from controls import ControlBinder
from entities import Snake, Food, BonusFood, PoisonFood
from ui import GameUI


class SnakeGame:
    """Main Snake Game class with full gameplay mechanics"""
    
    def __init__(self):
        import turtle as turtle_module
        
        self.screen = turtle_module.Screen()
        self.screen.title("Snake Game - Classic Arcade")
        self.screen.bgcolor(settings.BACKGROUND_COLOR)
        self.screen.setup(
            width=settings.WINDOW_WIDTH,
            height=settings.WINDOW_HEIGHT
        )
        self.screen.tracer(0)
        
        self.ui = GameUI(self.screen)
        self.animation_manager = AnimationManager(self.screen)
        self.admin_controller = AdminController()
        self.control_binder = ControlBinder(self.screen, self)
        
        self.snake = Snake()
        self.food = Food()
        self.bonus_food = BonusFood()
        self.poison_food = PoisonFood()
        
        self.direction = "stop"
        self.next_direction = "stop"
        
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.speed = settings.STARTING_SPEED
        self.combo = 0
        
        self.running = False
        self.paused = False
        self.game_started = False
        
        self.bonus_active = False
        self.bonus_deadline = 0
        self.poison_active = False
        self.poison_deadline = 0
        
        self.game_mode = None
        self.difficulty = None
        self.time_limit = 0
        self.time_remaining = 0
        self.start_time = 0
        self.foods_eaten = 0
        
        self.create_food()
        self.create_bonus_food()
        self.create_poison_food()
        self.bind_controls()
    
    # ---------------------------------------------------------
    # Screen setup
    # ---------------------------------------------------------
    
    def create_food(self):
        self.food = Food()
    
    def create_bonus_food(self):
        self.bonus_food = BonusFood()
    
    def create_poison_food(self):
        self.poison_food = PoisonFood()
    
    # ---------------------------------------------------------
    # UI methods
    # ---------------------------------------------------------
    
    def show_message(self, message, color=settings.TEXT_COLOR):
        self.ui.show_message(message, color)
    
    def clear_message(self):
        self.ui.clear_message()
    
    def update_scoreboard(self):
        state = {
            "score": self.score,
            "high_score": self.high_score,
            "level": self.level,
            "game_mode": self.game_mode,
            "difficulty": self.difficulty,
            "time_remaining": self.time_remaining,
            "admin_mode": self.admin_controller.admin_mode,
            "admin_points_per_food": self.admin_controller.admin_points_per_food,
            "admin_speed_multiplier": self.admin_controller.admin_speed_multiplier,
            "admin_animation_level": self.admin_controller.admin_animation_level,
        }
        self.ui.update_scoreboard(state)
    
    # ---------------------------------------------------------
    # Food management
    # ---------------------------------------------------------
    
    def get_random_position(self):
        while True:
            x = random.randrange(
                settings.GAME_LEFT + settings.GRID_SIZE,
                settings.GAME_RIGHT - settings.GRID_SIZE,
                settings.GRID_SIZE
            )
            
            y = random.randrange(
                settings.GAME_BOTTOM + settings.GRID_SIZE,
                settings.GAME_TOP - settings.GRID_SIZE,
                settings.GRID_SIZE
            )
            
            position_is_free = all(
                segment.distance(x, y) >= settings.GRID_SIZE
                for segment in self.snake
            )
            
            if position_is_free:
                return x, y
    
    def place_food(self, food_object):
        food_object.goto(self.get_random_position())
    
    def activate_bonus_food(self):
        self.bonus_active = True
        self.bonus_deadline = time.time() + settings.BONUS_FOOD_TIME / 1000
        self.place_food(self.bonus_food)
        self.bonus_food.show()
    
    def activate_poison_food(self):
        self.poison_active = True
        self.poison_deadline = time.time() + settings.BONUS_FOOD_TIME / 1500
        self.place_food(self.poison_food)
        self.poison_food.show()
    
    def update_bonus_food(self):
        if not self.bonus_active:
            return
        
        if time.time() >= self.bonus_deadline:
            self.bonus_active = False
            self.bonus_food.hide()
    
    def update_poison_food(self):
        if not self.poison_active:
            return
        
        if time.time() >= self.poison_deadline:
            self.poison_active = False
            self.poison_food.hide()
    
    # ---------------------------------------------------------
    # Movement
    # ---------------------------------------------------------
    
    def set_direction(self, new_direction):
        opposite_directions = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left"
        }
        
        if self.direction == "stop":
            self.next_direction = new_direction
            return
        
        if opposite_directions.get(self.direction) != new_direction:
            self.next_direction = new_direction
    
    def move_snake(self):
        self.direction = self.next_direction
        
        for index in range(len(self.snake) - 1, 0, -1):
            self.snake.segments[index].goto(self.snake.segments[index - 1].position())
        
        head = self.snake.head()
        
        if self.direction == "up":
            head.sety(head.ycor() + settings.GRID_SIZE)
        elif self.direction == "down":
            head.sety(head.ycor() - settings.GRID_SIZE)
        elif self.direction == "left":
            head.setx(head.xcor() - settings.GRID_SIZE)
        elif self.direction == "right":
            head.setx(head.xcor() + settings.GRID_SIZE)
    
    # ---------------------------------------------------------
    # Collision detection
    # ---------------------------------------------------------
    
    def hit_wall(self):
        head = self.snake.head()
        
        return (
            head.xcor() > settings.GAME_RIGHT - settings.GRID_SIZE
            or head.xcor() < settings.GAME_LEFT + settings.GRID_SIZE
            or head.ycor() > settings.GAME_TOP - settings.GRID_SIZE
            or head.ycor() < settings.GAME_BOTTOM + settings.GRID_SIZE
        )
    
    def hit_self(self):
        head = self.snake.head()
        
        for segment in self.snake.segments[1:]:
            if head.distance(segment) < settings.GRID_SIZE:
                return True
        
        return False
    
    # ---------------------------------------------------------
    # Scoring and levels
    # ---------------------------------------------------------
    
    def grow_snake(self):
        new_segment = self.snake.create_segment()
        new_segment.goto(self.snake.tail().position())
        self.snake.add_segment(new_segment)
        self.animation_manager.animate_snake_growth(new_segment)
    
    def increase_score(self, points):
        self.score += points
        
        if self.score > self.high_score:
            self.high_score = self.score
        
        if self.game_mode != "time_attack":
            new_level = self.score // 100 + 1
            
            if new_level > self.level:
                self.level = new_level
                self.speed = max(20, int(self.speed * 0.9))
                self.animation_manager.animate_level_up(self.level)
                self.screen.ontimer(self.clear_message, settings.LEVEL_UP_MESSAGE_DURATION)
        
        self.update_scoreboard()
    
    def check_food_collision(self):
        head = self.snake.head()
        
        if head.distance(self.food.turtle) < settings.GRID_SIZE:
            self.animation_manager.animate_food_pickup(self.food)
            self.animation_manager.pulse_effect(head)
            self.grow_snake()
            self.combo += 1
            self.foods_eaten += 1
            combo_multiplier = 1 + (self.combo * 0.1)
            points = int(
                self.admin_controller.admin_points_per_food * combo_multiplier 
                if self.admin_controller.admin_mode 
                else settings.NORMAL_FOOD_POINTS * combo_multiplier
            )
            self.increase_score(points)
            self.animation_manager.draw_score_popup(self.food.xcor(), self.food.ycor(), points)
            self.place_food(self.food)
            
            if random.random() < settings.BONUS_DROP_CHANCE and not self.bonus_active:
                self.activate_bonus_food()
            
            if random.random() < settings.POISON_DROP_CHANCE and not self.poison_active and self.foods_eaten > 5:
                self.activate_poison_food()
        
        if self.bonus_active and head.distance(self.bonus_food.turtle) < settings.GRID_SIZE:
            self.animation_manager.animate_food_pickup(self.bonus_food)
            self.animation_manager.pulse_effect(head)
            self.grow_snake()
            self.grow_snake()
            self.combo += 2
            bonus_points = int(
                settings.BONUS_FOOD_POINTS * (self.admin_controller.admin_points_per_food / settings.NORMAL_FOOD_POINTS)
            ) if self.admin_controller.admin_mode else settings.BONUS_FOOD_POINTS
            self.increase_score(bonus_points)
            self.animation_manager.draw_score_popup(self.bonus_food.xcor(), self.bonus_food.ycor(), bonus_points)
            
            self.bonus_active = False
            self.bonus_food.hide()
        
        if self.poison_active and head.distance(self.poison_food.turtle) < settings.GRID_SIZE:
            self.combo = 0
            poison_damage = settings.POISON_FOOD_POINTS
            self.increase_score(poison_damage)
            self.animation_manager.draw_score_popup(self.poison_food.xcor(), self.poison_food.ycor(), poison_damage)
            self.poison_active = False
            self.poison_food.hide()
    
    # ---------------------------------------------------------
    # Game state
    # ---------------------------------------------------------
    
    def game_over(self, reason):
        self.running = False
        self.direction = "stop"
        self.next_direction = "stop"
        
        self.show_message(
            f"{reason}\n"
            f"Final Score: {self.score}    Level: {self.level}\n"
            f"Food Eaten: {self.foods_eaten}\n"
            "Press R to return to menu",
            "#FF3131"
        )
    
    def toggle_pause(self):
        if not self.game_started or not self.running:
            return
        
        self.paused = not self.paused
        
        if self.paused:
            self.show_message("PAUSED\nPress P to continue", "#FFD700")
        else:
            self.clear_message()
    
    # ---------------------------------------------------------
    # Main game loop
    # ---------------------------------------------------------
    
    def start_game(self):
        self.game_started = True
        self.running = True
        self.paused = False
        self.reset_game()
        self.game_loop()
    
    def reset_game(self):
        self.snake.clear()
        
        self.score = 0
        self.level = 1
        self.direction = "stop"
        self.next_direction = "stop"
        self.bonus_active = False
        self.poison_active = False
        self.combo = 0
        self.foods_eaten = 0
        
        if self.game_mode == "time_attack":
            self.time_remaining = self.time_limit
            self.start_time = time.time()
        
        for index in range(settings.STARTING_LENGTH):
            segment = self.snake.create_segment(is_head=index == 0)
            segment.goto(-index * settings.GRID_SIZE, 0)
            self.snake.add_segment(segment)
        
        self.food.show()
        self.bonus_food.hide()
        self.poison_food.hide()
        
        self.place_food(self.food)
        self.clear_message()
        self.update_scoreboard()
    
    def game_loop(self):
        if self.game_mode == "time_attack":
            self.time_remaining = self.time_limit - (time.time() - self.start_time)
            
            if self.time_remaining <= 0:
                self.game_over("TIME'S UP!")
                return
        
        if self.running and not self.paused:
            if self.direction != "stop":
                self.move_snake()
                
                if self.hit_wall():
                    self.game_over("YOU HIT THE WALL")
                elif self.hit_self():
                    self.game_over("YOU HIT YOURSELF")
                else:
                    self.check_food_collision()
            else:
                if self.next_direction != "stop":
                    self.move_snake()
                    
                    if self.hit_wall():
                        self.game_over("YOU HIT THE WALL")
                    elif self.hit_self():
                        self.game_over("YOU HIT YOURSELF")
                    else:
                        self.check_food_collision()
            
            self.update_bonus_food()
            self.update_poison_food()
        
        self.screen.update()
        self.update_scoreboard()
        
        if self.running:
            self.screen.ontimer(self.game_loop, self.speed)
    
    def bind_controls(self):
        self.control_binder.bind()
