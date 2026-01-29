import arcade
from constants import PLAYER_SPEED, PLAYER_SCALE

class Dyno(arcade.Sprite):
    def __init__(self):
        super().__init__("images/dyno_1.png", scale=PLAYER_SCALE)
        self.center_x = 0
        self.center_y = 30
        self.speed_x = PLAYER_SPEED
        self.speed_y = 0
        self.moving_textures = [arcade.load_texture("images/dyno_1.png"), arcade.load_texture("images/dyno_2.png")]
        self.texture_update_number = 0
        self.time_since_last_face_update = 0
        self.update_interval = 0.2

    def update(self, delta_time, keys):
        self.change_x = self.speed_x
        self.change_y = self.speed_y
        if self.speed_x < 40:
            self.speed_x += 0.003

    def update_texture(self, delta_time: float = 1 / 60, update_texture_to_jump_held=False):
        if update_texture_to_jump_held:
            self.texture = arcade.load_texture("images/dyno.png")
        else:
            self.time_since_last_face_update += delta_time
            if self.time_since_last_face_update >= self.update_interval:
                self.time_since_last_face_update = 0
                self.texture = self.moving_textures[self.texture_update_number]
                if self.texture_update_number == 1:
                    self.texture_update_number = 0
                elif self.texture_update_number == 0:
                    self.texture_update_number = 1