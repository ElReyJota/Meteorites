import arcade

class Ship(arcade.Sprite):
    """ The main player, the ship, used to move around
    """


    def __init__(self, scaling):
        """ Initializes the ship to its sprite
        """
        super().__init__("./assets/ship.png", scaling)
