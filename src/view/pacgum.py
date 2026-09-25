from . import GameView
import numpy as np
from ..shared import Vector2D
from . import SpriteSheetManager


class Pacgums(GameView):

    def __init__(self, maze_width: int, maze_height: int,
                 pacgum_list: set[Vector2D],
                 super_pacgum_list: set[Vector2D],
                 sprite: SpriteSheetManager):

        super().__init__(maze_width, maze_height)
        self.pacgum_list = pacgum_list
        self.super_pacgum_list = super_pacgum_list
        self.sprite = sprite

    def render(self, dest_image_buffer: np.ndarray,
               dest_img_width: int) -> None:

        pos_x = self.x_start + self.sprite_size
        pos_y = self.y_start + self.sprite_size

        for pacgum in self.pacgum_list:
            dest_x = pos_x + pacgum.x * self.tile_size
            dest_y = pos_y + pacgum.y * self.tile_size
            self.put_sprite_in_image(dest_image_buffer,
                                     self.screen_width,
                                     dest_x, dest_y,
                                     self.sprite_size, self.sprite_size,
                                     self.sprite.get_sprite("pacgum_small"))

        for pacgum in self.super_pacgum_list:

            dest_x = pos_x + pacgum.x * self.tile_size
            dest_y = pos_y + pacgum.y * self.tile_size
            self.put_sprite_in_image(dest_image_buffer,
                                     self.screen_width,
                                     dest_x, dest_y,
                                     self.sprite_size, self.sprite_size,
                                     self.sprite.get_sprite("pacgum_large"))
