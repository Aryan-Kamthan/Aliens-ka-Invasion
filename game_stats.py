class GameStats():
    """Tracks Statistics for Alien Invasion."""

    def __init__(self, ai_settings):
        """Initialize statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False  # Start alien invasion in an inactive state
        self.high_score = 0  # It shall never be reset during a gameplay.

    def reset_stats(self):
        """Initialize Statistics that can change during game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1