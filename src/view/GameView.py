from . import Graphic
from . import SpriteSheetManager
from . import MazeRenderer
from mazegenerator import MazeGenerator
import screeninfo
from pygame import Surface


class GameView:

    def __init__(self, maze_width: int, maze_height: int) -> None:
        self.screen_width = screeninfo.get_monitors()[0].width
        self.screen_height = screeninfo.get_monitors()[0].height
        self.graphic = Graphic()
        self.screen = self.graphic.new_window(self.screen_width,
                                              self.screen_height)
        self.dest_img = self.graphic.new_image(self.screen_width,
                                               self.screen_height)
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.graphic = Graphic()
        self.scaling = self.graphic.get_scaling(maze_width, maze_height,
                                                self.screen_width,
                                                self.screen_height)

        self.tile_size = self.graphic.get_tile_size(self.maze_width,
                                                    self.maze_height,
                                                    self.screen_width,
                                                    self.screen_height)
        self.sprite_size = self.tile_size // 3 + 1

        self.usable_width = self.graphic.get_usable_width(self.screen_width)
        self.usable_height = self.graphic.get_usable_height(self.screen_height)
        self.half_img_width = (self.usable_width // 2 +
                               self.graphic.get_padding() // 2)
        self.half_img_height = (self.usable_height // 2 +
                                self.graphic.get_padding() // 2)

        self.x_start = self.half_img_width - int((self.maze_width / 2)
                                                 * self.tile_size)
        self.y_start = self.half_img_height - int((self.maze_height / 2)
                                                  * self.tile_size)

    def blit_and_update(self, img: Surface, dest_screen: Surface):

        self.graphic.blit_img(img, dest_screen, (0, 0))
        self.graphic.update_window()
