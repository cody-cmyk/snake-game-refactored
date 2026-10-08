import turtle


class GameUI:
    def __init__(self, screen):
        self.screen = screen

        self.border_pen = turtle.Turtle()
        self.border_pen.hideturtle()
        self.border_pen.speed(0)
        self.border_pen.color("#E6F1FF")
        self.border_pen.pensize(3)

        self.score_writer = turtle.Turtle()
        self.score_writer.hideturtle()
        self.score_writer.penup()
        self.score_writer.color("#FFFFFF")

        self.message_writer = turtle.Turtle()
        self.message_writer.hideturtle()
        self.message_writer.penup()
        self.message_writer.color("#FFFFFF")

        self.help_writer = turtle.Turtle()
        self.help_writer.hideturtle()
        self.help_writer.penup()
        self.help_writer.color("#B8C7CC")

        self.admin_indicator = turtle.Turtle()
        self.admin_indicator.hideturtle()
        self.admin_indicator.penup()
        self.admin_indicator.color("#FF00FF")

        self.draw_border()

    def draw_border(self):
        self.border_pen.penup()
        self.border_pen.goto(-350, -260)
        self.border_pen.pendown()
        self.border_pen.goto(350, -260)
        self.border_pen.goto(350, 260)
        self.border_pen.goto(-350, 260)
        self.border_pen.goto(-350, -260)

        self.help_writer.goto(0, -335)
        self.help_writer.write(
            "Move: Arrow Keys / WASD    |    Pause: P    |    Restart: R    |    Admin: A+C",
            align="center",
            font=("Arial", 12, "normal")
        )

    def show_message(self, message, color="#FFFFFF"):
        self.message_writer.clear()
        self.message_writer.color(color)
        self.message_writer.goto(0, -20)
        self.message_writer.write(
            message,
            align="center",
            font=("Arial", 26, "bold")
        )

    def clear_message(self):
        self.message_writer.clear()

    def update_scoreboard(self, game_state):
        self.score_writer.clear()
        self.score_writer.goto(0, 320)

        if game_state["game_mode"] == "time_attack":
            self.score_writer.write(
                f"Score: {game_state['score']}    "
                f"High Score: {game_state['high_score']}    "
                f"Time: {max(0, int(game_state['time_remaining']))}s    "
                f"Difficulty: {game_state['difficulty'].upper()}",
                align="center",
                font=("Arial", 18, "bold")
            )
        else:
            self.score_writer.write(
                f"Score: {game_state['score']}    "
                f"High Score: {game_state['high_score']}    "
                f"Level: {game_state['level']}    "
                f"Mode: {game_state['game_mode'].upper() if game_state['game_mode'] else 'CLASSIC'}    "
                f"Difficulty: {game_state['difficulty'].upper() if game_state['difficulty'] else 'NORMAL'}",
                align="center",
                font=("Arial", 18, "bold")
            )

        if game_state.get("admin_mode"):
            self.admin_indicator.clear()
            self.admin_indicator.goto(-400, 320)
            self.admin_indicator.write(
                f"[ADMIN] Points: {game_state['admin_points_per_food']} | Speed: {game_state['admin_speed_multiplier']}x | Anim: {game_state['admin_animation_level']}",
                align="left",
                font=("Arial", 12, "bold")
            )
        else:
            self.admin_indicator.clear()


# Compatibility alias for the original code expectations
GameUICompat = GameUI
