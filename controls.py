import settings


class AdminController:
    def __init__(self):
        self.admin_mode = False
        self.admin_points_per_food = settings.NORMAL_FOOD_POINTS
        self.admin_speed_multiplier = 1.0
        self.admin_animation_level = 1

    def clamp_points(self, value):
        return max(
            settings.ADMIN_MIN_POINTS,
            min(settings.ADMIN_MAX_POINTS, value)
        )

    def clamp_speed(self, value):
        return max(
            settings.ADMIN_MIN_SPEED,
            min(settings.ADMIN_MAX_SPEED, round(value, 1))
        )

    def clamp_animation(self, value):
        return max(
            settings.ADMIN_ANIMATION_MIN,
            min(settings.ADMIN_ANIMATION_MAX, int(value))
        )

    def adjust_points(self, amount):
        self.admin_points_per_food = self.clamp_points(self.admin_points_per_food + amount)

    def adjust_speed(self, amount):
        self.admin_speed_multiplier = self.clamp_speed(self.admin_speed_multiplier + amount)

    def set_animation(self, level):
        self.admin_animation_level = self.clamp_animation(level)

    def state(self):
        return {
            "admin_mode": self.admin_mode,
            "admin_points_per_food": self.admin_points_per_food,
            "admin_speed_multiplier": self.admin_speed_multiplier,
            "admin_animation_level": self.admin_animation_level,
        }
