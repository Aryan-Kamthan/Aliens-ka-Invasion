"""Most of this class is like the Ship class except for the placement of the alien"""
import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet"""

    def __init__(self, ai_settings, screen):
        """Initialize the alien and its starting position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each new alien at the top left corner of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw alien at it's current location"""
        self.screen.blit(self.image, self.rect)

    def check_edge(self):
        """Returns True if alien fleet is on the edge of the screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:  # Checks for the right edge
            return True
        elif self.rect.left <= 0:  # Checks for the left edge
            return True

    def update(self):
        """Moves the alien to right or left."""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)  # We track alien's exact position by self.x
        self.rect.x = self.x  # We than use self.x to update the position of alien's rect

