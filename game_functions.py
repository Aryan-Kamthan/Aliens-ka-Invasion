import sys   # We will use sys to exit the game when player quits.
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep  # To pause the game we will use sleep() function


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fires a bullet if limit is not reached yet"""
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)  # Creates a new bullet and adds it to bullets group
        bullets.add(new_bullet)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Responds to key presses"""
    if event.key == pygame.K_RIGHT:  # If right arrow is pressed
        ship.moving_right = True  # Moves the ship to right
    elif event.key == pygame.K_LEFT:  # If left arrow is pressed
        ship.moving_left = True  # Moves the ship to left
    elif event.key == pygame.K_SPACE:  # If SPACE BAR is pressed
        fire_bullet(ai_settings, screen, ship, bullets)  # Fires a bullet


def check_keyup_events(event, ship):
    """Responds to key releases"""
    if event.key == pygame.K_RIGHT:  # If Right arrow is realsed
        ship.moving_right = False  # Stops moving ship
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets,  mouse_x, mouse_y):
    """Start a new game when the player clicks play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)  # If the x and y coordinates of mouse overlaps the play_button
    if button_clicked and not stats.game_active:  # makes play button active only if game is inactive
        pygame.mouse.set_visible(False)  # makes the mouse invisible while playing the game
        # Reset the game statistics
        stats.reset_stats()
        stats.game_active = True
        ai_settings.initialize_dynamic_settings()

        # Reset the scoreboard images.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Responds to keypress and mouse events"""
    for event in pygame.event.get():  # Watch for keyboard and mouse events,
                # any keyboard or mouse event will cause the for loop to run
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # If a keyboard key is pressed
           check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:  # If a keyboard key is realised
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:  # If a mouse key is pressed
            mouse_x, mouse_y = pygame.mouse.get_pos()  # returns the x and y  coordinates of the mouse in form of tuple. to restrict activating game over play button only.
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets,  mouse_x, mouse_y)


def update_screen(ai_settings, screen, stats, sb, ship, alien, bullets, play_button):
    """Update images on the screen and flip to a new screen"""

    # Redraw the screen during each pass
    screen.fill(ai_settings.bg_color)

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullets()

    ship.blitme()  # To show ship on screen
    alien.draw(screen)  # To show alien on screen

    # Draw the score information
    sb.show_score()

    # Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    # Make most recently drawn screen visible
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Updates the position of the bullets and gets rid of the bullets which left screen"""
    # Update bullet positions
    bullets.update()
    # to get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:  # To check if a bullet is out of the screen
            bullets.remove(bullet)  # Delete that bullet

    # Check for any bullets that have hit aliens and remove them.
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Responds to bullet alien collisions and repopulate the fleet if empty"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    """sprite.groupcollide() method compares each bullet rect with each aliens's rect and return a dictionary that has 
    bullet as key and aliens as values which have collided. The two TRUE arguments at the end signals that both the 
    collided elements should be deleted"""

    if collisions:  # Add points
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            check_high_score(stats, sb)

    # repopulating the fleet
    if (len(aliens)) == 0:
        bullets.empty()  # Destroy existing bullets
        ai_settings.increase_speed()  # Speed up the game
        create_fleet(ai_settings, screen, ship, aliens)  # Create new fleet
        stats.level += 1  # Increase the level
        sb.prep_level()  # Draw the new level image


def get_number_aliens_x(ai_settings, alien_width):
    """Determines the number of aliens that fit in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width  # Calculates the available space in each row when margin between alien and edge is one alien width.
    number_alien_x = int(available_space_x / (2 * alien_width))  # Determines the number of aliens in each row based on available_space_x.
    return number_alien_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows that fit on the screen"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in a row"""
    alien = Alien(ai_settings, screen)  # Creates an alien which is not a part of fleet just for calculations
    alien_width = alien.rect.width  # Stores the width of alien
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Creates a full fleet of aliens"""
    alien = Alien(ai_settings, screen)  # Creates an alien which is not a part of fleet just for calculations
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # Creates the first row of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """Responds appropriately if any alien touches the edge of screen"""
    for alien in aliens.sprites():
        if alien.check_edge():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change it's direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed  # drops fleet
    ai_settings.fleet_direction *= -1  # Changes Direction


def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Check if the fleet is at an edge and then Update the positions of all aliens in the fleet"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Looks for alien-ship collision
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
    """The method collideany() takes two attribute a sprite and a group. 
    It looks for any member of Group that collides with the Sprite and exits the loop as soon as it finds out any collision 
    between group member and sprite. Here it loops through aliens group and returns the first alien that collides with the sprite ship """

    # Look for alien hitting the bottom of screen
    check_alien_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Responds to Ship being hit by an alien"""
    if stats.ships_left > 0:
        stats.ships_left -= 1  # Decrement Ship_left

        # Update Scoreboard
        sb.prep_ships()

        # Empty the list of aliens and bullets on screen
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #Pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)  # makes mouse visible


def check_alien_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Check if an alien has reached the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:  # If alien reaches the bottom of screen
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def check_high_score(stats, sb): # this function will be called each time an alien is hit to check for change in high score through bullet_alien_collision function
    """Check to see if there is a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
