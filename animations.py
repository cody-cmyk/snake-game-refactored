import time
import turtle

import settings


class AnimationManager:
    def __init__(self, screen):
        self.screen = screen

    def animate_food_pickup(self, food):
        if self.screen is None:
            return

        original_size = food.turtle.shapesize()
        for i in range(settings.ANIMATION_PICKUP_STEPS):
            shrink = 1 - i * settings.ANIMATION_PICKUP_SCALE
            food.turtle.shapesize(
                original_size[0] * shrink,
                original_size[1] * shrink
            )
            self.screen.update()
            time.sleep(0.02)

    def animate_snake_growth(self, segment):
        if self.screen is None:
            return

        segment.shapesize(0.3, 0.3)
        for i in range(settings.ANIMATION_GROW_STEPS):
            growth = 0.3 + (i * settings.ANIMATION_GROW_SCALE)
            segment.shapesize(growth, growth)
            self.screen.update()
            time.sleep(0.02)
        segment.shapesize(1.0, 1.0)

    def animate_level_up(self, level):
        if self.screen is None:
            return

        for color in settings.ANIMATION_LEVEL_COLORS * 2:
            self.screen.update()
            time.sleep(0.15)

    def draw_score_popup(self, x, y, points):
        if self.screen is None:
            return

        popup = turtle.Turtle()
        popup.speed(0)
        popup.hideturtle()
        popup.penup()
        popup.color("#FFD700")
        popup.goto(x, y)
        popup.write(f"+{points}", align="center", font=("Arial", 14, "bold"))

        for i in range(settings.ANIMATION_POPUP_STEPS):
            popup.goto(x, y + (i * settings.ANIMATION_POPUP_OFFSET))
            self.screen.update()
            time.sleep(0.05)

        popup.hideturtle()
