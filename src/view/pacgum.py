import numpy as np
import pygame
from numpy import ndarray
from .sprite_sheet_manager import SpriteSheetManager
from .sprite_validator import SpriteData
from .mlx_wrapper import load_sprite, to_buffer
from ..model import GameBoard


class Pacgums:

    def __init__(self, game_board: GameBoard,
                 pacgums_sprites: SpriteSheetManager,
                 window: pygame.Surface):

        self.pacgums_pos = game_board.pacgum_pos
        self.super_pacgums_pos = game_board.super_pacgums_pos
        self.pacgums_sprites = pacgums_sprites.sprites
        self.tile_size = self.get_tile_size_pacgums(
            game_board.maze.width,
            game_board.maze.height,
            window.get_width(),
            window.get_height()
        )
        self.sprite_size = self.tile_size // 3
        center_x = window.get_width() // 2
        center_y = window.get_height() // 2
        self.x_start = center_x - (game_board.maze.width * self.tile_size) // 2
        self.y_start = center_y - (
            game_board.maze.height * self.tile_size) // 2

    @staticmethod
    def _get_padding() -> int:
        return 500

    def get_tile_size_pacgums(self, obj_width: int, obj_height: int,
                              screen_width: int, screen_height: int) -> int:
        usable_width = screen_width - self._get_padding()
        usable_height = screen_height - self._get_padding()
        px_tile_width = usable_width // obj_width
        px_tile_height = usable_height // obj_height
        raw_size = min(px_tile_height, px_tile_width)
        tile_size = (raw_size // 3) * 3
        return max(tile_size, 3)

    def put_sprite_in_image(self, dest_image_buffer: ndarray,
                            dest_image_width: int,
                            dest_x: int, dest_y: int,
                            dest_w: int, dest_h: int,
                            sprite_data: SpriteData) -> None:

        sheet_surface = load_sprite(str(sprite_data.image_path))
        sheet_buffer = to_buffer(sheet_surface)
        sheet_width = sheet_surface.get_width()

        x_gap = np.arange(dest_w)
        y_gap = np.arange(dest_h)

        src_x = sprite_data.x + (sprite_data.w * x_gap) // dest_w
        src_y = sprite_data.y + (sprite_data.h * y_gap) // dest_h

        sprite_pos_1d = ((src_y)[:, None] * sheet_width
                         + (src_x)).ravel()
        image_pos_1d = ((dest_y + y_gap)[:, None] * dest_image_width
                        + (dest_x + x_gap)).ravel()

        dest_image_buffer[image_pos_1d] = sheet_buffer[sprite_pos_1d]

    def render(self, dest_image_buffer: ndarray,
               dest_img_width: int) -> None:

        pos_x = self.x_start + self.sprite_size
        pos_y = self.y_start + self.sprite_size

        for pacgum in self.pacgums_pos:
            dest_x = pos_x + pacgum.x * self.tile_size
            dest_y = pos_y + pacgum.y * self.tile_size
            self.put_sprite_in_image(dest_image_buffer,
                                     dest_img_width,
                                     dest_x, dest_y,
                                     self.sprite_size, self.sprite_size,
                                     self.pacgums_sprites["pacgum_small"])

        for pacgum in self.super_pacgums_pos:
            dest_x = pos_x + pacgum.x * self.tile_size
            dest_y = pos_y + pacgum.y * self.tile_size
            self.put_sprite_in_image(dest_image_buffer,
                                     dest_img_width,
                                     dest_x, dest_y,
                                     self.sprite_size, self.sprite_size,
                                     self.pacgums_sprites["pacgum_large"])
