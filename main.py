import arcade
from src.ship import Ship
from src.star import Star
from src.meteor import Meteor
from src.missile import Missile
import math
import random

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Meteorites"
SCALING = 2

class Meteorites(arcade.Window):
    """
    Main application class.
    """
    paused = False

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # If you have sprite lists, you should create them here,
        # and set them to None
        self.meteorites_list = arcade.SpriteList()
        self.stars_list = arcade.SpriteList()
        self.missiles_list = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

    def setup(self):
        """Get the game ready to play
        """
        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

        # Set up the player
        self.player = Ship(SCALING)
        self.player.center_y = self.height / 2
        self.player.left = self.width / 2
        self.all_sprites.append(self.player)

        # Sets up the background stars and the waves of meteorites
        self.add_wave(60)
        arcade.schedule(self.add_star, 0.25)
        arcade.schedule(self.add_wave, 15)
        self.music = arcade.load_sound("assets/Titanomachia II.wav")
        arcade.play_sound(self.music)
        arcade.schedule(self.background_music, 212)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()

        # Call draw() on all your sprite lists below
        arcade.start_render()
        self.stars_list.draw()
        self.missiles_list.draw()
        self.player.draw()
        self.meteorites_list.draw()

    def on_update(self, delta_time):
        """Update the positions and statuses of all game objects
        If paused, do nothing
        Arguments:
            delta_time {float} -- Time since the last update
        """

        # If paused, don't update anything
        if self.paused:
            arcade.unschedule(self.add_star)
            arcade.unschedule(self.add_wave)
            return

        # If player hit close game
        if self.player.collides_with_list(self.meteorites_list):
            arcade.close_window()

        # If Missile Hits Then Delete Missile and Destroy Meteor
        for missile in self.missiles_list:
            check = missile.collides_with_list(self.meteorites_list)
            if check:
                missile.delete()
                for meteor in check:
                    meteor.downgrade()

        # Update everything
        self.all_sprites.update()

        # Keep the player on screen
        if self.player.top > self.height:
            self.player.top = self.height
        if self.player.right > self.width:
            self.player.right = self.width
        if self.player.bottom < 0:
            self.player.bottom = 0
        if self.player.left < 0:
            self.player.left = 0

    def on_key_press(self, key, key_modifiers):
        """Handle user keyboard input
        Q: Quit the game
        P: Pause/Unpause the game
        W/A/S/D: Move Up, Left, Down, Right
        Arrows: Move Up, Left, Down, Right

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if key == arcade.key.Q:
            # Quit immediately
            arcade.close_window()

        if key == arcade.key.P:
            self.paused = not self.paused
        
        if key == arcade.key.P and not self.paused:
            arcade.schedule(self.add_star, 0.25)
            arcade.schedule(self.add_wave, 60)

        if key == arcade.key.W or key == arcade.key.UP:
            self.player.change_y = 2
            self.player.angle = 45

        if key == arcade.key.S or key == arcade.key.DOWN:
            self.player.change_y = -2
            self.player.angle = 225

        if key == arcade.key.A or key == arcade.key.LEFT:
            self.player.change_x = -2
            self.player.angle = 135

        if key == arcade.key.D or key == arcade.key.RIGHT:
            self.player.change_x = 2
            self.player.angle = -45

    def on_key_release(self, key, key_modifiers):
        """Undo movement vectors when movement keys are released

        Arguments:
            symbol {int} -- Which key was pressed
            modifiers {int} -- Which modifiers were pressed
        """
        if (
            key == arcade.key.W
            or key == arcade.key.S
            or key == arcade.key.UP
            or key == arcade.key.DOWN
        ):
            self.player.change_y = 0

        if (
            key == arcade.key.A
            or key == arcade.key.D
            or key == arcade.key.LEFT
            or key == arcade.key.RIGHT
        ):
            self.player.change_x = 0

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.add_missile(x, y)

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            arcade.unschedule(self.add_missile)

    def add_star(self, delta_time: float):
        """Adds a new star to the screen

        Arguments:
            delta_time {float} -- How much time has passed since the last call
        """

        # Create the star sprite
        star = Star(random.randint(20, 150) / 100)

        # Set its position to a random height and off screen right
        star.left = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 80)
        star.top = random.randint(10, self.height - 10)

        # Set its speed to a random speed heading left
        star.velocity = (random.randint(-3, -1), 0)

        # Add it to the sprite lists
        self.stars_list.append(star)
        self.all_sprites.append(star)

    def add_wave(self, delta_time: float):
        """Adds a new enemy to the screen

        Arguments:
            delta_time {float} -- How much time as passed since the last call
        """

        # Creates all the meteors of the wave
        for i in range(1, 11, 1):
            meteor = Meteor(SCALING, SCREEN_HEIGHT, SCREEN_WIDTH)

            # Sets the meteor to the left of the screen unseen
            meteor.left = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 80)
            meteor.top = random.randint(10, self.height - 10)

            # Gives a random velocity to the left
            meteor.velocity = (random.randint(-5, -3), 0)

            # Adds them to the sprite list
            self.meteorites_list.append(meteor)
            self.all_sprites.append(meteor)

    def add_missile(self, target_x, target_y):
        """Adds a new missile to the screen

        Arguments:
            delta_time {float} -- How much time as passed since the last call
        """

        # Creates the missile
        missile = Missile(SCALING, SCREEN_HEIGHT, SCREEN_WIDTH)

        # Sets the missile from the player
        missile.center_y = self.player.center_y
        missile.center_x = self.player.center_x

        # Finds the distance between the target and point
        d = math.sqrt((target_x - missile.center_x)**2 + (target_y - missile.center_y)**2)
        # Finds the velocity required to reach the target and as a base puts 5
        x = 5 * (target_x - missile.center_x) / d
        y = 5 * (target_y - missile.center_y) / d
        missile.velocity = (x, y)

        # Puts the sprite on the list
        self.missiles_list.append(missile)
        self.all_sprites.append(missile)

    def background_music(self, delta_time: float):
        """Adds background music to the game
        """
        arcade.play_sound(self.music)

def main():
    """ Main function """
    game = Meteorites(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()
    


if __name__ == "__main__":
    main()