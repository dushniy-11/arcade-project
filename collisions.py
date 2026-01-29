import arcade
from constants import COLLISION_SCALE


class Cactus(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(":resources:images/tiles/cactus.png", scale=COLLISION_SCALE)
        self.center_x = x
        self.center_y = y


class Pterodactyl(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("images/pterodactyl.png", scale=COLLISION_SCALE)
        self.center_x = x
        self.center_y = y
