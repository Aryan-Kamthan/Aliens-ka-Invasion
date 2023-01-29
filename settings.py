# A class to store all the settings
class Settings():
    def __init__(self): # To initialize game's  static setting
        # Screen settings
        self.screen_width = 1080
        self.screen_height = 640
        self.bg_color = (230, 230, 230)

        # Ship Setting
        self.ship_speed_factor = 1.1  # On each keystroke ship moves 1,5 pixel rather than 1 px
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed_factor = 1
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 3  # This limits the player to shoot 5  bullets at a time on screen

        # ALien Settings
        self.alien_speed_factor = 0.8
        self.fleet_drop_speed = 5  # It controls how quickly fleet drops when it reaches either edge
        # Fleet direction of 1 represents right and -1 represents left
        self.fleet_direction = 1

        # how quickly the game speeds up.
        self.speedup_scale = 1.01

        # How quickly the alien point vali=ues increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that changes through the game"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increases the speed setting and point value"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
