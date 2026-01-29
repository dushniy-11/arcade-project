import arcade
import random
import os
from dyno import Dyno
from collisions import Pterodactyl, Cactus
from constants import *
from pyglet.graphics import Batch
from dp_operations import Database

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.WHITE)
        self.world_camera = arcade.camera.Camera2D()
        self.in_update_player_texture = True
        self.start_game, self.end_game = True, False
        self.count = 0
        self.jump_sound = arcade.load_sound("sounds/jump.wav")
        self.end_game_sound = arcade.load_sound("sounds/end_game.mp3")

    def setup(self):
        self.keys_pressed = set()
        self.players_list = arcade.SpriteList()
        self.collisions_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.player = Dyno()
        self.players_list.append(self.player)

        self.background_1 = arcade.Sprite("images/background.png", scale=1)
        self.background_2 = arcade.Sprite("images/background.png", scale=1)
        self.background_3 = arcade.Sprite("images/background.png", scale=1)
        self.background_1.center_x = 300
        self.background_1.center_y = 50
        self.background_2.center_x = 900
        self.background_2.center_y = 50
        self.background_3.center_x = 1500
        self.background_3.center_y = 50
        self.background_list.append(self.background_1)
        self.background_list.append(self.background_2)
        self.background_list.append(self.background_3)

        self.engine = arcade.PhysicsEnginePlatformer(
            self.player,
            self.background_list,
            gravity_constant=GRAVITY
        )

        self.batch = Batch()
        self.start_text = arcade.Text("Нажми H, чтобы начать!", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                      arcade.color.RED, font_size=30, anchor_x="center", batch=self.batch)

    def on_draw(self):
        self.clear()
        self.background_list.draw()
        self.players_list.draw()
        self.collisions_list.draw()
        self.world_camera.use()
        self.batch.draw()

    def on_update(self, delta_time):
        if self.start_game:
            self.player.alpha = 0
            return
        else:
            self.player.alpha = 255

        if self.end_game:
            self.end_text = arcade.Text(f"LOSE; count = {self.count // 100}", SCREEN_WIDTH / 2 + self.player.center_x,
                                        SCREEN_HEIGHT / 2,
                                        arcade.color.RED, font_size=30, anchor_x="center", batch=self.batch)
            self.batch.draw()
            return

        self.engine.update()
        self.players_list.update(delta_time, self.keys_pressed)
        self.collisions_list.update()
        self.make_collision()

        position = (
            self.player.center_x + 400,
            self.player.center_y
        )
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            position,
            CAMERA_LERP,
        )

        for element in self.collisions_list:
            if arcade.check_for_collision(self.player, element):
                self.end_game = True
                arcade.play_sound(self.end_game_sound)
                database = Database(os.getlogin(), self.count // 100)
                database.check_user()
                self.player.texture = arcade.load_texture("images/dyno_end.png")
            if element.center_x < self.player.center_x - (SCREEN_WIDTH // 2 + SCREEN_WIDTH // 2):
                element.remove_from_sprite_lists()

        for element in self.background_list:
            max_x = max(object.center_x for object in self.background_list)
            if element.center_x < self.player.center_x - (SCREEN_WIDTH // 2 + SCREEN_WIDTH // 1.5):
                element.center_x = max_x + 1150

        if self.in_update_player_texture:
            self.player.update_texture()

        if self.player.center_y == 223.25:
            self.in_update_player_texture = True

        self.count += 1

    def on_key_press(self, key, modifiers):
        if key == arcade.key.H:
            self.start_game = False
        if self.end_game or self.start_game:
            return
        if key == arcade.key.W:
            if self.engine.can_jump():
                self.player.change_y = JUMP_SPEED
                arcade.play_sound(self.jump_sound)
            self.player.update_texture(update_texture_to_jump_held=True)
            self.in_update_player_texture = False
        if key == arcade.key.H:
            self.start_game = False

    def make_collision(self):
        if len(self.collisions_list) == 0:
            if random.random() < 0.4:
                x = self.player.center_x + (750 * random.randint(1, 2))
                y1 = 210
                y2 = 250
                y3 = 290
                cactus1 = Cactus(x, y1)
                cactus2 = Cactus(x, y2)
                cactus3 = Cactus(x, y3)
                self.collisions_list.append(cactus1)
                self.collisions_list.append(cactus2)
                self.collisions_list.append(cactus3)
            elif 0.4 <= random.random() <= 0.8:
                x = self.player.center_x + (100 * random.randint(8, 10))
                y1 = 210
                y2 = 250
                cactus1 = Cactus(x, y1)
                cactus2 = Cactus(x, y2)
                self.collisions_list.append(cactus1)
                self.collisions_list.append(cactus2)
            else:
                x = self.player.center_x + (200 * random.randint(4, 6))
                y = self.player.center_y + (15 * random.randint(1, 5))
                pterodactyl = Pterodactyl(x, y)
                self.collisions_list.append(pterodactyl)
