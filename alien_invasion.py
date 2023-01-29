import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from pygame.sprite import Group # Group contains a datastructure like lists with some extra functionalites that helps in managing bullets that are already fired.

# Initialize game and create the screen also initializes Settings


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))  # SCREEN is a surface that creates display window,

    # The SURFACE is automatically redrawn at each iteration of loop
    pygame.display.set_caption("Aliens ka Invasion")

    # Maje a Play Button.
    play_button = Button(ai_settings, screen, "Play")

    # Creates an instance to store the game statistics and create a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Make a ship
    ship = Ship(ai_settings,screen)

    # Make a group to store bullets in.
    bullets = Group()

    # Make an empty group to hold all the aliens in the game.
    aliens = Group()

    # Create a fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)

    bg_color = (230, 230, 230)  # Set the background color

    # Start the main loop
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)  # It will always run

        if stats.game_active:  # It will run only when game is active
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)  # It will always run


run_game()
