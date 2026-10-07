import pygame
from numpy import ndarray
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from ..model import GameBoard
from ..shared import GhostState
from .displayer_utils import DisplayerUtils
from ..shared import Direction
from ..model.entities import Entity


class Entities:

    def __init__(self, game_board: GameBoard,
                 sprites: SpriteSheetsManager,
                 screen_width: int,
                 screen_height: int) -> None:
        self.sprites = sprites
        self.maze_grid: list[list[int]] = game_board.maze.grid
        self.utils = DisplayerUtils()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.tile_size = self.utils.get_tile_size_maze(
            game_board.maze.width,
            game_board.maze.height,
            self.screen_width,
            self.screen_height
        )
        self.sprite_size = int(self.tile_size / 3)
        center_x = int(self.screen_width / 2)
        center_y = int(self.screen_height / 2)
        self.x_start = int(center_x -
                           (game_board.maze.width * self.tile_size) / 2)
        self.y_start = int(center_y - (
            game_board.maze.height * self.tile_size) / 2)
        self.game_board = game_board

    def render(self, dest_img_buffer: ndarray,
               dest_img_width: int, game_board: GameBoard) -> None:
        pass

    def select_animation(self, dir: Direction, entity: Entity) -> str:
        return f"{entity.__class__.__name__}.{dir._name_}"


class PacmanView(Entities):

    def render(self, dest_img_buffer: ndarray,
               dest_img_width: int, game_board: GameBoard) -> None:

        pacman = game_board.player

        dir_sprite = self.select_animation(pacman.move_dir_state, pacman)

        pos_x = int(self.x_start + self.sprite_size / 2)
        pos_y = int(self.y_start + self.sprite_size / 2)

        dest_y = int(pos_y + game_board.player.move_pixel_y * self.tile_size)
        dest_x = int(pos_x + game_board.player.move_pixel_x * self.tile_size)

        if not game_board.player.is_moving():
            animation = self.sprites.animations[dir_sprite]
            sprite_name = animation.frames[2]
        else:
            animation = self.sprites.animations[dir_sprite]
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


class GhostView(Entities):

    def render(self, dest_img_buffer: ndarray,
               dest_img_width: int, game_board: GameBoard) -> None:

        ghost_dict = game_board.ghosts

        for ghost in ghost_dict.values():

            pos_x = self.x_start + self.sprite_size // 2
            pos_y = self.y_start + self.sprite_size // 2

            sprites_name = self.select_animation(ghost.move_dir_state, ghost)

            if ghost.state == GhostState.FRIGHTENED:
                sprites_name = "ghost_scared_blue"
            elif ghost.state == GhostState.FRIGHTENED_END:
                sprites_name = "ghost_scared_flash"

            animation = self.sprites.animations[sprites_name]
            animation_time = ghost.animation_timer * 1000
            frame_index = int(
                animation_time / animation.speed) % len(animation.frames)
            sprite_name = animation.frames[frame_index]
            dest_y = int(pos_y + ghost.move_pixel_y * self.tile_size)
            dest_x = int(pos_x + ghost.move_pixel_x * self.tile_size)

            if ghost.state == GhostState.EATEN:
                sprite_name = "ghost_eyes_up"

            self.utils.put_sprite_in_image(
                dest_img_buffer,
                dest_img_width,
                dest_x,
                dest_y,
                self.sprite_size * 2,
                self.sprite_size * 2,
                self.sprites.sprites[sprite_name],
            )
