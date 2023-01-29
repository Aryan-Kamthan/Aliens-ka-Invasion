import pygame.font  # It lets pygame render text to screen
# pygame works with text by rendering the string we write as image.


class Button():
    def __init__(self, ai_settings, screen, msg):
        """Initialize the button attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Set the dimension and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)  # It renders text to screen. None argument uses sysyem font and 48 is font size

        # Set the buttons rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Button message
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turns the message into rendered imge and centers it on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)  # renders text to image
        self. msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)  # Draw a blank button
        self.screen.blit(self.msg_image, self.msg_image_rect)  # Draw message