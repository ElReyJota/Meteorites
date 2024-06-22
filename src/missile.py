import arcade

class Missile(arcade.Sprite):
    """ The missile, used to destroy meteorites
    Attributes:
        screen_height (int): How tall the screen is
        screen_width (int): How wide the screen is
    """
    screen_height = 0
    screen_width = 0

    def __init__(self, scaling, screen_height, screen_width):
        """Initializes the missile to its sprite, also updates the screen values
        """
        super().__init__("./assets/missile.png", scaling)
        self.screen_height = screen_height
        self.screen_width = screen_width

    def update(self):
        """Update the position of the sprite
        When it moves off screen remove it
        """

        # Move the sprite
        super().update()

        # Remove if off the screen
        if (self.center_x < 0 or self.center_x > self.screen_width or
            self.center_y < 0 or self.center_y > self.screen_height):
            self.remove_from_sprite_lists()
    
    def delete(self):
        """Deletes the missile
        """
        self.remove_from_sprite_lists()