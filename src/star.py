import arcade
import random

class Star(arcade.Sprite):
    """ The background star, for the game to look pretty
    """

    def __init__(self, scaling):
        """ Initializes the star sprite and its angle
        """
        super().__init__(f"./assets/star{random.randint(1, 4)}.png", scaling)
        self.angle = random.randint(0, 360)

    def update(self):
        """Update the position of the sprite
        When it moves off screen to the left, remove it
        """

        # Move the sprite
        super().update()

        # Remove if off the screen
        if self.right < 0:
            self.remove_from_sprite_lists()