from . import Graphic
import screeninfo
from pygame import Surface
from .sprite_sheet_manager import SpriteModel
import numpy as np


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

        self.tile_size = self.get_tile_size(self.maze_width,
                                            self.maze_height,
                                            self.screen_width,
                                            self.screen_height)
        self.sprite_size = self.tile_size // 3 + 1

        self.usable_width = self.get_usable_width(self.screen_width)
        self.usable_height = self.get_usable_height(self.screen_height)
        self.half_img_width = (self.usable_width // 2 +
                               self.graphic.get_padding() // 2)
        self.half_img_height = (self.usable_height // 2 +
                                self.graphic.get_padding() // 2)

        self.x_start = self.half_img_width - int((self.maze_width / 2)
                                                 * self.tile_size)
        self.y_start = self.half_img_height - int((self.maze_height / 2)
                                                  * self.tile_size)

    def get_usable_width(self, screen_width: int) -> int:
        padding = self.graphic.get_padding()
        return (screen_width - padding)

    def get_usable_height(self, screen_height: int) -> int:
        padding = self.graphic.get_padding()
        return (screen_height - padding)

    def get_tile_size(self, maze_width: int, maze_height: int,
                      screen_width: int, screen_height: int) -> int:

        usable_width = self.get_usable_width(screen_width)
        usable_height = self.get_usable_height(screen_height)
        px_tile_width = usable_width // maze_width
        px_tile_height = usable_height // maze_height
        return min(px_tile_height, px_tile_width)

    def put_sprite_in_image(self, dest_image_buffer: np.ndarray,
                            dest_image_width: int,
                            dest_x: int, dest_y: int,
                            dest_w: int, dest_h: int,
                            sprite_data: SpriteModel) -> None:

        x_gap = np.arange(dest_w)
        y_gap = np.arange(dest_h)

        src_x = (sprite_data.width * x_gap) // dest_w
        src_y = (sprite_data.height * y_gap) // dest_h

        offset_x = sprite_data.pos_x
        offset_y = sprite_data.pos_y

        sprite_pos_1d = ((offset_y + src_y)[:, None] * sprite_data.file_width
                         + (offset_x + src_x)).ravel()
        image_pos_1d = ((dest_y + y_gap)[:, None] * dest_image_width
                        + (dest_x + x_gap)).ravel()

        dest_image_buffer[image_pos_1d] = sprite_data.buffer[sprite_pos_1d]

    def blit_and_update(self, img: Surface, dest_screen: Surface):

        self.graphic.blit_img(img, dest_screen, (0, 0))
        self.graphic.update_window()
