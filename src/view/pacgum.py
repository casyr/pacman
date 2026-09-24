from . import Graphic
from . import GameView
from numpy import ndarray
from ..shared import Vector2D
from . import SpriteModel

class Pacgums(GameView):

    def __init__(self, maze_width: int, maze_height: int,
                 pacgum_list: set[Vector2D], sprite: SpriteModel):
        super().__init__(maze_width, maze_height)
        self.pacgum_list = pacgum_list
        self.sprite = sprite

    def render(self, dest_image_buffer: ndarray,
               dest_img_width: int) -> None:
        for pacgum in self.pacgum_list:

            dest_x = self.x_start + pacgum.x * self.tile_size
            dest_y = self.y_start + pacgum.y * self.tile_size
            self.put_sprite_in_image(dest_image_buffer,
                                     self.screen_width, 
                                     dest_x, dest_y,
                                     self.tile_size, self.tile_size,
                                     self.sprite)
