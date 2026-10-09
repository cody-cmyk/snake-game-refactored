import turtle


class Menu:
    """Main game menu with improved UI and navigation"""
    
    def __init__(self, screen):
        self.screen = screen
        self.current_menu = "main"
        
        # Menu turtles
        self.title_turtle = turtle.Turtle()
        self.title_turtle.hideturtle()
        self.title_turtle.penup()
        self.title_turtle.color("#00FF00")
        
        self.menu_turtle = turtle.Turtle()
        self.menu_turtle.hideturtle()
        self.menu_turtle.penup()
        self.menu_turtle.color("#FFFFFF")
        
        self.instruction_turtle = turtle.Turtle()
        self.instruction_turtle.hideturtle()
        self.instruction_turtle.penup()
        self.instruction_turtle.color("#FFFF00")
        
        self.highlight_turtle = turtle.Turtle()
        self.highlight_turtle.hideturtle()
        self.highlight_turtle.penup()
        self.highlight_turtle.color("#FF6600")
    
    def clear_screen(self):
        """Clear all text from menu"""
        self.title_turtle.clear()
        self.menu_turtle.clear()
        self.instruction_turtle.clear()
        self.highlight_turtle.clear()
    
    def show_main_menu(self, callback_dict):
        """Display main menu"""
        self.clear_screen()
        self.current_menu = "main"
        
        self.title_turtle.goto(0, 250)
        self.title_turtle.write(
            "ARCADE GAMES",
            align="center",
            font=("Arial", 40, "bold")
        )
        
        self.menu_turtle.goto(0, 120)
        self.menu_turtle.write(
            "1: SNAKE GAME\n\n"
            "2: TETRIS\n\n"
            "3: SETTINGS\n\n"
            "4: QUIT",
            align="center",
            font=("Arial", 24, "normal")
        )
        
        self.instruction_turtle.goto(0, -280)
        self.instruction_turtle.write(
            "Press 1, 2, 3, or 4 to select",
            align="center",
            font=("Arial", 12, "normal")
        )
        
        self.screen.listen()
        self.screen.onkeypress(callback_dict.get("snake"), "1")
        self.screen.onkeypress(callback_dict.get("tetris"), "2")
        self.screen.onkeypress(callback_dict.get("settings"), "3")
        self.screen.onkeypress(callback_dict.get("quit"), "4")
    
    def show_snake_mode_menu(self, callback_dict):
        """Display snake game mode selection"""
        self.clear_screen()
        self.current_menu = "snake_mode"
        
        self.title_turtle.goto(0, 250)
        self.title_turtle.write(
            "SNAKE GAME - SELECT MODE",
            align="center",
            font=("Arial", 30, "bold")
        )
        
        self.menu_turtle.goto(0, 120)
        self.menu_turtle.write(
            "1: CLASSIC MODE\n\n"
            "2: TIME ATTACK MODE\n\n"
            "3: SURVIVAL MODE\n\n"
            "4: BACK",
            align="center",
            font=("Arial", 20, "normal")
        )
        
        self.instruction_turtle.goto(0, -280)
        self.instruction_turtle.write(
            "Press 1, 2, 3, or 4 to select | ESC to go back",
            align="center",
            font=("Arial", 12, "normal")
        )
        
        self.screen.listen()
        self.screen.onkeypress(callback_dict.get("classic"), "1")
        self.screen.onkeypress(callback_dict.get("time_attack"), "2")
        self.screen.onkeypress(callback_dict.get("survival"), "3")
        self.screen.onkeypress(callback_dict.get("back"), "4")
        self.screen.onkeypress(callback_dict.get("back"), "Escape")
    
    def show_difficulty_menu(self, mode, callback_dict):
        """Display difficulty selection"""
        self.clear_screen()
        self.current_menu = "difficulty"
        
        self.title_turtle.goto(0, 250)
        self.title_turtle.write(
            f"SELECT DIFFICULTY\n{mode.upper()}",
            align="center",
            font=("Arial", 28, "bold")
        )
        
        self.menu_turtle.goto(0, 120)
        self.menu_turtle.write(
            "1: EASY\n\n"
            "2: MEDIUM\n\n"
            "3: HARD",
            align="center",
            font=("Arial", 22, "normal")
        )
        
        self.instruction_turtle.goto(0, -280)
        self.instruction_turtle.write(
            "Easy: Slow speed, longer time | Hard: Fast speed, less time",
            align="center",
            font=("Arial", 12, "normal")
        )
        
        self.screen.listen()
        self.screen.onkeypress(callback_dict.get("easy"), "1")
        self.screen.onkeypress(callback_dict.get("medium"), "2")
        self.screen.onkeypress(callback_dict.get("hard"), "3")
    
    def show_settings_menu(self, admin_controller, callback_dict):
        """Display settings menu"""
        self.clear_screen()
        self.current_menu = "settings"
        
        self.title_turtle.goto(0, 250)
        self.title_turtle.write(
            "SETTINGS & ADMIN PANEL",
            align="center",
            font=("Arial", 30, "bold")
        )
        
        self.menu_turtle.goto(0, 100)
        self.menu_turtle.write(
            f"1: ADJUST POINTS (Current: {admin_controller.admin_points_per_food})\n\n"
            f"2: ADJUST SPEED (Current: {admin_controller.admin_speed_multiplier}x)\n\n"
            f"3: ANIMATION LEVEL (Current: {admin_controller.admin_animation_level})\n\n"
            f"4: BACK TO MENU",
            align="center",
            font=("Arial", 18, "normal")
        )
        
        self.instruction_turtle.goto(0, -280)
        self.instruction_turtle.write(
            "Use arrow keys or +/- to adjust values",
            align="center",
            font=("Arial", 12, "normal")
        )
        
        self.screen.listen()
        self.screen.onkeypress(callback_dict.get("adjust_points"), "1")
        self.screen.onkeypress(callback_dict.get("adjust_speed"), "2")
        self.screen.onkeypress(callback_dict.get("adjust_animation"), "3")
        self.screen.onkeypress(callback_dict.get("back"), "4")
    
    def show_adjust_points_menu(self, current_value, callback_dict):
        """Display points adjustment menu"""
        self.clear_screen()
        
        self.title_turtle.goto(0, 250)
        self.title_turtle.write(
            "ADJUST POINTS PER FOOD",
            align="center",
            font=("Arial", 28, "bold")
        )
        
        self.menu_turtle.goto(0, 100)
        self.menu_turtle.write(
            f"CURRENT VALUE: {current_value}\n\n"
            "+ Key: Increase by 10\n"
            "- Key: Decrease by 10\n"
            "ENTER: Confirm\n"
            "ESC: Cancel",
            align="center",
            font=("Arial", 20, "normal")
        )
        
        self.screen.listen()
        self.screen.onkeypress(lambda: callback_dict.get("increase")(), "plus")
        self.screen.onkeypress(lambda: callback_dict.get("increase")(), "=")
        self.screen.onkeypress(lambda: callback_dict.get("decrease")(), "minus")
        self.screen.onkeypress(lambda: callback_dict.get("decrease")(), "-")
        self.screen.onkeypress(callback_dict.get("confirm"), "Return")
        self.screen.onkeypress(callback_dict.get("cancel"), "Escape")
    
    def show_adjust_speed_menu(self, current_value, callback_dict):
        """Display speed adjustment menu"""
        self.clear_screen()
        
        self.title_turtle.goto(0, 250)
        self.title_turtle.write(
            "ADJUST SPEED MULTIPLIER",
            align="center",
            font=("Arial", 28, "bold")
        )
        
        self.menu_turtle.goto(0, 100)
        self.menu_turtle.write(
            f"CURRENT VALUE: {current_value:.1f}x\n\n"
            "+ Key: Increase by 0.1x\n"
            "- Key: Decrease by 0.1x\n"
            "ENTER: Confirm\n"
            "ESC: Cancel",
            align="center",
            font=("Arial", 20, "normal")
        )
        
        self.screen.listen()
        self.screen.onkeypress(lambda: callback_dict.get("increase")(), "plus")
        self.screen.onkeypress(lambda: callback_dict.get("increase")(), "=")
        self.screen.onkeypress(lambda: callback_dict.get("decrease")(), "minus")
        self.screen.onkeypress(lambda: callback_dict.get("decrease")(), "-")
        self.screen.onkeypress(callback_dict.get("confirm"), "Return")
        self.screen.onkeypress(callback_dict.get("cancel"), "Escape")
    
    def show_adjust_animation_menu(self, current_level, callback_dict):
        """Display animation level adjustment menu"""
        self.clear_screen()
        
        anim_names = ["", "NORMAL", "ENHANCED", "ULTRA"]
        current_name = anim_names[current_level] if current_level < len(anim_names) else "UNKNOWN"
        
        self.title_turtle.goto(0, 250)
        self.title_turtle.write(
            "ANIMATION LEVEL",
            align="center",
            font=("Arial", 28, "bold")
        )
        
        self.menu_turtle.goto(0, 100)
        self.menu_turtle.write(
            f"CURRENT LEVEL: {current_name}\n\n"
            "1: NORMAL (Standard)\n"
            "2: ENHANCED (Smooth trails)\n"
            "3: ULTRA (Trails + Effects)\n"
            "ENTER: Back",
            align="center",
            font=("Arial", 18, "normal")
        )
        
        self.screen.listen()
        self.screen.onkeypress(lambda: callback_dict.get("set_animation")(1), "1")
        self.screen.onkeypress(lambda: callback_dict.get("set_animation")(2), "2")
        self.screen.onkeypress(lambda: callback_dict.get("set_animation")(3), "3")
        self.screen.onkeypress(callback_dict.get("back"), "Return")
    
    def show_game_start_screen(self, mode, difficulty, time_limit, callback_dict):
        """Display pre-game screen before starting"""
        self.clear_screen()
        
        self.title_turtle.goto(0, 250)
        self.title_turtle.write(
            f"{mode.upper()} MODE",
            align="center",
            font=("Arial", 32, "bold")
        )
        
        if mode == "time_attack":
            self.menu_turtle.goto(0, 120)
            self.menu_turtle.write(
                f"Difficulty: {difficulty.upper()}\n\n"
                f"Time Limit: {time_limit} seconds\n\n"
                "Collect food and maximize your score!\n\n"
                "Press ENTER to start",
                align="center",
                font=("Arial", 18, "normal")
            )
        else:
            self.menu_turtle.goto(0, 120)
            self.menu_turtle.write(
                f"Difficulty: {difficulty.upper()}\n\n"
                "Collect food and grow your snake!\n"
                "Get combos for bonus points!\n"
                "Avoid walls and yourself!\n\n"
                "Press ENTER to start",
                align="center",
                font=("Arial", 18, "normal")
            )
        
        self.instruction_turtle.goto(0, -280)
        self.instruction_turtle.write(
            "Arrow Keys or WASD to move | P to pause | M for menu",
            align="center",
            font=("Arial", 12, "normal")
        )
        
        self.screen.listen()
        self.screen.onkeypress(callback_dict.get("start"), "Return")
    
    def show_tetris_start_screen(self, callback_dict):
        """Display pre-tetris screen before starting"""
        self.clear_screen()
        
        self.title_turtle.goto(0, 250)
        self.title_turtle.write(
            "TETRIS - BLOCK STACK CHALLENGE",
            align="center",
            font=("Arial", 28, "bold")
        )
        
        self.menu_turtle.goto(0, 80)
        self.menu_turtle.write(
            "Stack the falling blocks and complete lines!\n\n"
            "Arrow Keys or A/D: Move\n"
            "Space or Up: Rotate\n"
            "Down: Hard Drop\n"
            "P: Pause | Q: Quit | M: Menu\n\n"
            "Press ENTER to start",
            align="center",
            font=("Arial", 16, "normal")
        )
        
        self.screen.listen()
        self.screen.onkeypress(callback_dict.get("start"), "Return")
