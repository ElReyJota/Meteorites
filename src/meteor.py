import arcade
import random

class Meteor(arcade.Sprite):
    """The main obstacle and enemy of the player
    Attributes:
        
        type (int): Which type of meteor is it, there is 3
        tier (int): Which tier of meteor is it, there is 3, it is also its hitpoints
        screen_height (int): How tall the screen is
        screen_width (int): How wide the screen is
    """
    type = 0
    tier = 0
    screen_height = 0
    screen_width = 0

    def __init__(self, scaling, screen_height, screen_width):
        """Initializes the meteor to its type, tier, angle and sprite. Also updates screen values
        """
        self.type = random.randint(1, 3)
        self.tier = random.randint(1, 3)
        super().__init__(f"./assets/{self.tier}{self.type}meteor.png", scaling)
        self.angle = random.randint(0, 360)
        self.screen_height = screen_height
        self.screen_width = screen_width

    def update(self):
        """Update the position of the sprite
        When it moves off screen to the left, remove it
        """

        # Move the sprite
        super().update()

        # Remove if off the screen
        if self.right < -80:
            self.left = random.randint(self.screen_width, self.screen_width + 80)
            self.angle = random.randint(0, 360)

    def downgrade(self):
        """Downgrades the meteor if hit or destroys it if too small
        """
        self.tier -= 1
        match self.tier:
            case 0:
                self.remove_from_sprite_lists()