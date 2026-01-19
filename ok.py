import arcade
import random


SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
SCREEN_TITLE = "DиноZаврик"
PLAYER_SPEED = 10
JUMP_SPEED = 300
PLAYER_SCALE = 0.3
COLLISION_SCALE = 0.4
GRAVITY = 9
CAMERA_LERP = 0.15


class Cactus(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(":resources:images/tiles/cactus.png", scale=COLLISION_SCALE)
        self.center_x = x
        self.center_y = y

class Pterodactyle(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("pterodactyl.png", scale=COLLISION_SCALE)
        self.center_x = x
        self.center_y = y

class Dyno(arcade.Sprite):
    def __init__(self):
        super().__init__("dyno.png", scale=PLAYER_SCALE)
        self.center_x = 0
        self.center_y = 30
        self.speed_x = PLAYER_SPEED
        self.speed_y = 0

    def update(self, delta_time, keys):
        self.change_x = self.speed_x
        self.change_y = self.speed_y
        if self.speed_x < 30:
            self.speed_x += 0.003


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.WHITE)
        self.world_camera = arcade.camera.Camera2D()
        self.end_game = False

    def setup(self):
        self.keys_pressed = set()
        self.players_list = arcade.SpriteList()
        self.collisions_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.player = Dyno()
        self.players_list.append(self.player)

        self.background_1 = arcade.Sprite("background.png", scale=1)
        self.background_2 = arcade.Sprite("background.png", scale=1)
        self.background_3 = arcade.Sprite("background.png", scale=1)
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

    def on_draw(self):
        self.clear()
        self.background_list.draw()
        self.players_list.draw()
        self.collisions_list.draw()
        self.world_camera.use()

    def on_update(self, delta_time):
        if self.end_game:
            return
        self.engine.update()
        self.players_list.update(delta_time, self.keys_pressed)
        self.collisions_list.update()
        self.make_cactus()
        self.make_pterodactyl()

        position = (
            self.player.center_x,
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
            if element.center_x < self.player.center_x - (SCREEN_WIDTH // 2 + SCREEN_WIDTH // 2):
                element.remove_from_sprite_lists()

        for element in self.background_list:
            max_x = max(object.center_x for object in self.background_list)
            if element.center_x < self.player.center_x - (SCREEN_WIDTH // 2 + SCREEN_WIDTH // 1.5):
                element.center_x = max_x + 1150

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            if self.engine.can_jump():
                self.player.change_y = JUMP_SPEED

    def make_cactus(self):
        if len(self.collisions_list) < 1:
            if random.random() > 0.4:
                x = self.player.center_x + (100 * random.randint(4, 8))
                y = 210
                cactus = Cactus(x, y)
                self.collisions_list.append(cactus)

    def make_pterodactyl(self):
        if len(self.collisions_list) < 1:
            if random.random() < 0.4:
                x = self.player.center_x + (100 * random.randint(4, 8))
                y = self.player.center_y + (40 * random.randint(1, 3))
                pterodactyle = Pterodactyle(x, y)
                self.collisions_list.append(pterodactyle)

def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
