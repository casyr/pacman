import pygame
from numpy import ndarray
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from ..model import GameBoard
from .displayer_utils import DisplayerUtils


class Entities:

    def __init__(self, game_board: GameBoard,
                 sprites: SpriteSheetsManager,
                 window: pygame.Surface):
        self.sprites = sprites
        self.maze_grid: list[list[int]] = game_board.maze.grid
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


class Pacman(Entities):

    def render(self, dest_img_buffer: ndarray,
               dest_img_width: int,
               game_board: GameBoard,
               window: pygame.Surface) -> None:

        pos_x = self.x_start + self.sprite_size - 8
        pos_y = self.y_start + self.sprite_size - 8

        dest_x = int(pos_x + game_board.player.current_pos_x * self.tile_size)
        dest_y = int(pos_y + game_board.player.current_pos_y * self.tile_size)

        self.utils.put_sprite_in_image(dest_img_buffer,
                                       dest_img_width,
                                       dest_x, dest_y,
                                       self.sprite_size * 2,
                                       self.sprite_size * 2,
                                       self.sprites.sprites["pacman_right_1"])


class Ghost(Entities):

    def render(self, dest_img_buffer: ndarray,
               dest_img_width: int,
               game_board: GameBoard,
               window: pygame.Surface) -> None:

        pos_x = self.x_start + self.sprite_size
        pos_y = self.y_start + self.sprite_size

        for ghost in game_board.ghosts:

            dest_x = pos_x + ghost.current_pos_x * self.tile_size
            dest_y = pos_y + ghost.current_pos_y * self.tile_size

            put_sprite_in_image = self.utils.put_sprite_in_image

            put_sprite_in_image(dest_img_buffer,
                                dest_img_width,
                                dest_x, dest_y,
                                self.sprite_size * 2,
                                self.sprite_size * 2,
                                self.sprites.sprites["pacman_right_1"])


class Pinky(Entities):

    def render(self, dest_img_buffer: ndarray,
               dest_img_width: int,
               game_board: GameBoard,
               window: pygame.Surface) -> None:

        pos_x = self.x_start + self.sprite_size
        pos_y = self.y_start + self.sprite_size

        dest_x = pos_x + game_board.player.current_pos_x * self.tile_size
        dest_y = pos_y + game_board.player.current_pos_y * self.tile_size

        self.utils.put_sprite_in_image(dest_img_buffer,
                                       dest_img_width,
                                       dest_x, dest_y,
                                       self.sprite_size * 2,
                                       self.sprite_size * 2,
                                       self.sprites.sprites["pacman_right_1"])


class Inky(Entities):

    def render(self, dest_img_buffer: ndarray,
               dest_img_width: int,
               game_board: GameBoard,
               window: pygame.Surface) -> None:

        pos_x = self.x_start + self.sprite_size
        pos_y = self.y_start + self.sprite_size

        dest_x = pos_x + game_board.player.current_pos_x * self.tile_size
        dest_y = pos_y + game_board.player.current_pos_y * self.tile_size

        self.utils.put_sprite_in_image(dest_img_buffer,
                                       dest_img_width,
                                       dest_x, dest_y,
                                       self.sprite_size * 2,
                                       self.sprite_size * 2,
                                       self.sprites.sprites["pacman_right_1"])


class Clyde(Entities):

    def render(self, dest_img_buffer: ndarray,
               dest_img_width: int,
               game_board: GameBoard,
               window: pygame.Surface) -> None:

        pos_x = self.x_start + self.sprite_size
        pos_y = self.y_start + self.sprite_size

        dest_x = pos_x + game_board.player.current_pos_x * self.tile_size
        dest_y = pos_y + game_board.player.current_pos_y * self.tile_size
        dest_y = pos_y + game_board.player.current_pos_y * self.tile_size

        self.utils.put_sprite_in_image(dest_img_buffer,
                                       dest_img_width,
                                       dest_x, dest_y,
                                       self.sprite_size * 2,
                                       self.sprite_size * 2,
                                       self.sprites.sprites["pacman_right_1"])
