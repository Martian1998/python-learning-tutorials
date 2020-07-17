"""
Move with a Sprite Animation

Simple program to show basic sprite usage.

Artwork from http://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_move_animation
"""
import arcade
import random
import os
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Move with a Sprite Animation Example"

COIN_SCALE = 0.1
COIN_COUNT = 10
CHARACTER_SCALING = 1

MOVEMENT_SPEED = 5
UPDATES_PER_FRAME = 7

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True)
    ]


class PlayerCharacter(arcade.Sprite):
    def __init__(self):

        # Set up parent class
        super().__init__()

        
        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0

        # Track out state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        self.scale = CHARACTER_SCALING

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # --- Load Textures ---

        # Images from Kenney.nl's Asset Pack 3
        # main_path = "./png/Run"
        # main_path = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"
        # main_path = ":resources:images/animated_characters/female_person/femalePerson"
        # main_path = ":resources:images/animated_characters/male_person/malePerson"
        # main_path = ":resources:images/animated_characters/male_adventurer/maleAdventurer"
        # main_path = ":resources:images/animated_characters/zombie/zombie"
        main_path = ":resources:images/animated_characters/robot/robot"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        # self.idle_texture_pair = load_texture_pair(f"./png/Idle (1).png")

        # Load textures for walking
        self.walk_textures = []
        for i in range(8):
            # texture = load_texture_pair(f"{main_path} ({i}).png")
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

    def update_animation(self, delta_time: float = 1/60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """
        Initializer
        """
        super().__init__(width, height, title)
        
        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        """ Set up the game and initialize the variables. """

        self.game_state = "intro"
        
        self.intro = None
        self.end = None

        self.setupUpdated = True

        # Sprite lists
        self.player_list = None
        self.coin_list = None

        self.background = None

        # Set up the player
        self.score = 0
        self.player = None
        arcade.set_background_color(arcade.color.AMAZON)


    def setup(self):
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.player = PlayerCharacter()

        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player.scale = 0.5

        self.player_list.append(self.player)

        for i in range(COIN_COUNT):
            coin = arcade.AnimatedTimeSprite(scale=0.5)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            robot = random.randint(1,3)
            coin.textures = []
            for i in range(8):
                coin.textures.append(arcade.load_texture(f"./PNG_Animations/Robot{robot}/01_Idle/idle_00{i}.png"))
            coin.scale = COIN_SCALE
            coin.cur_texture_index = random.randrange(len(coin.textures))

            self.coin_list.append(coin)

        # Set the background color
        self.background = arcade.load_texture("./game_bg.png")
        # arcade.set_background_color(arcade.color.APRICOT)
        self.intro = arcade.load_texture("./intro.png")
        self.end = arcade.load_texture("./end.png")
        self.setupUpdated = True
        print(f"setup {self.game_state}")


    def on_draw(self):
        """
        Render the screen.
        """
        # print(f"on draw {self.game_state}")
        # This command has to happen before we start drawing
        arcade.start_render()
        if self.game_state == "intro":
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.intro)
        
        elif self.game_state == "end":
            arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.end)

        elif self.game_state == "running" and self.setupUpdated:
            arcade.draw_lrwh_rectangle_textured(0, 0,
                                                SCREEN_WIDTH, SCREEN_HEIGHT,
                                                self.background)

            # Draw all the sprites.
            self.coin_list.draw()
            self.player_list.draw()

            # Put the text on the screen.
            output = f"Score: {self.score}"
            arcade.draw_text(output, 10, 20, arcade.color.RED, 14)


    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.UP:
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED
        elif key == arcade.key.ENTER and self.game_state == "intro":
            self.setupUpdated = False
            self.game_state = "running"
            time.sleep(0.5)
            self.setup()
        elif key == arcade.key.ENTER and self.game_state == "end":
            self.setupUpdated = False
            self.game_state = "intro"
            time.sleep(0.5)
            self.setup()        

    def on_key_release(self, key, modifiers):
        """
        Called when the user releases a key.
        """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        self.coin_list.update()
        self.coin_list.update_animation()
        self.player_list.update()
        self.player_list.update_animation()

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player, self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for coin in hit_list:
            coin.remove_from_sprite_lists()
            self.player.scale += 0.1
            self.score += 1
        
        if len(self.coin_list) == 0:
            self.game_state = "end"


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()