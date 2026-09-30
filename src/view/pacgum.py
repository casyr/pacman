import numpy as np
import pygame
from numpy import ndarray
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from ..parsing.sprite_validator import SpriteData
from ..model import GameBoard
from .game_view import GameView


class Pacgums(GameView):

    def __init__(self, game_board: GameBoard,
                 pacgums_sprites: SpriteSheetsManager,
                 window: pygame.Surface):

        self.pacgums_pos = game_board.pacgum_pos
        self.super_pacgums_pos = game_board.super_pacgums_pos
        self.pacgums_sprites = pacgums_sprites.sprites
        self.tile_size = self.get_tile_size_maze(
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

    def put_sprite_in_image(self, dest_image_buffer: np.ndarray,
                            dest_image_width: int,
                            dest_x: int, dest_y: int,
                            dest_w: int, dest_h: int,
                            sprite_data: SpriteData) -> None:

        x_gap = np.arange(dest_w)
        y_gap = np.arange(dest_h)

        src_x = (sprite_data.coords.w * x_gap) // dest_w
        src_y = (sprite_data.coords.h * y_gap) // dest_h

        sprite_pos_1d = ((src_y)[:, None] *
                         sprite_data.coords.w + src_x).ravel()
        image_pos_1d = ((dest_y + y_gap)[:, None] *
                        dest_image_width + (dest_x + x_gap)).ravel()

        sprite_pixels = sprite_data.buffer[sprite_pos_1d]

        mask = sprite_pixels != 0

        dest_image_buffer[image_pos_1d[mask]] = sprite_pixels[mask]

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
