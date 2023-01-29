import pygame
from pygame.sprite import Sprite # using Sprite we can group related elements together and act on all grouped elements at once.


class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self, ai_settings, screen, ship):
        """Creates a bullet object at ship's current position"""
        super(Bullet, self).__init__()
        self.screen = screen

        # Creates a bullet rect at (0,0) i.e top left corner of screen and then set it's correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height) #We build a rect frrom scratch usung pygame.Rect
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Stores the bullet position as decimal value
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Moves the bullet on the screen"""
        # Update the decimal position of the bullets
        self.y -= self.speed_factor

        # Update the rect position
        self.rect.y = self.y

    def draw_bullets(self):
        """Draw the bullets to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)