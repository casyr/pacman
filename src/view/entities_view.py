import pygame
from numpy import ndarray
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from ..model import GameBoard
from ..shared import GhostName, GhostState
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

    def _render_ghost(self, dest_img_buffer: ndarray,
                      dest_img_width: int, game_board: GameBoard,
                      ghost_name: GhostName, sprite_name: str) -> None:
        pos_x = self.x_start + self.sprite_size - 8
        pos_y = self.y_start + self.sprite_size - 8

        for ghost in game_board.ghosts:
            if ghost.name != ghost_name:
                continue

            if ghost.state == GhostState.FRIGHTENED:
                sprite_name = "ghost_scared_blue_1"
            elif ghost.state == GhostState.EATEN:
                sprite_name = "ghost_eyes_right"

            dest_y = int(pos_y + ghost.move_pixel_y * self.tile_size)
            dest_x = int(pos_x + ghost.move_pixel_x * self.tile_size)
            self.utils.put_sprite_in_image(
                dest_img_buffer,
                dest_img_width,
                dest_x,
                dest_y,
                self.sprite_size * 2,
                self.sprite_size * 2,
                self.sprites.sprites[sprite_name],
            )


class PacmanView(Entities):

    def render(self, dest_img_buffer: ndarray,
               dest_img_width: int,
               game_board: GameBoard,
               window: pygame.Surface) -> None:

        pos_x = self.x_start + self.sprite_size - 8
        pos_y = self.y_start + self.sprite_size - 8

        dest_y = int(pos_y + game_board.player.move_pixel_y * self.tile_size)
        dest_x = int(pos_x + game_board.player.move_pixel_x * self.tile_size)

        if not game_board.player.is_moving():
            animation = self.sprites.animations["pacman_walk_right"]
            sprite_name = animation.frames[2]
        else:
            animation = self.sprites.animations["pacman_walk_right"]
            animation_time = game_board.player.animation_timer * 1000
            frame_index = int(
                animation_time / animation.speed) % len(animation.frames)
            sprite_name = animation.frames[frame_index]

        if game_board.player.is_dying:
            death_animation = self.sprites.animations["pacman_die"]
            death_time = game_board.player.death_elapsed * 1000
            frame_index = min(
                    int(death_time / death_animation.speed),
                    len(death_animation.frames) - 1
                )
            sprite_name = death_animation.frames[frame_index]

        self.utils.put_sprite_in_image(dest_img_buffer,
                                       dest_img_width,
                                       dest_x, dest_y,
                                       self.sprite_size * 2,
                                       self.sprite_size * 2,
                                       self.sprites.sprites[sprite_name])


class BlinkyView(Entities):

    def render(self, dest_img_buffer: ndarray,
               dest_img_width: int,
               game_board: GameBoard,
               window: pygame.Surface) -> None:

        self._render_ghost(
            dest_img_buffer, dest_img_width, game_board,
            GhostName.BLINKY, "ghost_blinky_right_1")


class PinkyView(Entities):

    def render(self, dest_img_buffer: ndarray,
               dest_img_width: int,
               game_board: GameBoard,
               window: pygame.Surface) -> None:

        self._render_ghost(
            dest_img_buffer, dest_img_width, game_board,
            GhostName.PINKY, "ghost_pinky_right_1")


class InkyView(Entities):

    def render(self, dest_img_buffer: ndarray,
               dest_img_width: int,
               game_board: GameBoard,
               window: pygame.Surface) -> None:

        self._render_ghost(
            dest_img_buffer, dest_img_width, game_board,
            GhostName.INKY, "ghost_inky_right_1")


class ClydeView(Entities):

    def render(self, dest_img_buffer: ndarray,
               dest_img_width: int,
               game_board: GameBoard,
               window: pygame.Surface) -> None:

        self._render_ghost(
            dest_img_buffer, dest_img_width, game_board,
            GhostName.CLYDE, "ghost_clyde_right_1")
