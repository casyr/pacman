import pygame
from numpy import ndarray
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from ..model import GameBoard
from .game_view import GameView
from .displayer_utils import DisplayerUtils


class Pacgums(GameView):

    def __init__(self, game_board: GameBoard,
                 pacgums_sprites: SpriteSheetsManager,
                 window: pygame.Surface):

        self.pacgums_pos = game_board.pacgum_pos
        self.super_pacgums_pos = game_board.super_pacgums_pos
        self.pacgums_sprites = pacgums_sprites.sprites
        self.utils = DisplayerUtils()
        self.tile_size = self.utils.get_tile_size_maze(
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

    def render(self, dest_image_buffer: ndarray,
               dest_img_width: int) -> None:

        pos_x = self.x_start + self.sprite_size
        pos_y = self.y_start + self.sprite_size

        for pacgum in self.pacgums_pos:
            dest_x = pos_x + pacgum.x * self.tile_size
            dest_y = pos_y + pacgum.y * self.tile_size
            self.utils.put_sprite_in_image(dest_image_buffer,
                                           dest_img_width,
                                           dest_x, dest_y,
                                           self.sprite_size, self.sprite_size,
                                           self.pacgums_sprites["pacgum_small"]
                                           )

        for pacgum in self.super_pacgums_pos:
            dest_x = pos_x + pacgum.x * self.tile_size
            dest_y = pos_y + pacgum.y * self.tile_size
            self.utils.put_sprite_in_image(dest_image_buffer,
                                           dest_img_width,
                                           dest_x, dest_y,
                                           self.sprite_size, self.sprite_size,
                                           self.pacgums_sprites["pacgum_large"]
                                           )
