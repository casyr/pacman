import pygame
import numpy as np
from enum import Enum
from typing import Any
from numpy import ndarray
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from ..parsing.sprite_validator import SpriteData
from ..model import GameBoard
from ..shared.geometry import Wall
from .game_view import GameView


class CornerWall(Enum):
    NORTH_WEST = Wall.NORTH.value + Wall.WEST.value
    NORTH_EAST = Wall.NORTH.value + Wall.EAST.value
    SOUTH_EAST = Wall.SOUTH.value + Wall.EAST.value
    SOUTH_WEST = Wall.SOUTH.value + Wall.WEST.value


class Maze(GameView):

    def __init__(self, game_board: GameBoard,
                 maze_sprites: SpriteSheetsManager,
                 window: pygame.Surface):
        self.maze_sprites = maze_sprites.sprites
        self.maze_grid: list[list[int]] = game_board.maze.grid
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

    def straight_wall_chooser(self, sprites: list[Any],
                              is_top: bool, is_bottom: bool,
                              is_left: bool, is_right: bool) -> None:
        if is_left:
            sprite = self.maze_sprites["wall_double_vertical_left"]
        else:
            sprite = self.maze_sprites["wall_single_vertical_left"]
        sprites[Wall.WEST.value] = sprite

        if is_right:
            sprite = self.maze_sprites["wall_double_vertical_right"]
        else:
            sprite = self.maze_sprites["wall_single_vertical_right"]
        sprites[Wall.EAST.value] = sprite

        if is_top:
            sprite = self.maze_sprites["wall_double_horizontal_top"]
        else:
            sprite = self.maze_sprites["wall_single_horizontal_top"]
        sprites[Wall.NORTH.value] = sprite

        if is_bottom:
            sprite = self.maze_sprites["wall_double_horizontal_bottom"]
        else:
            sprite = self.maze_sprites["wall_single_horizontal_bottom"]
        sprites[Wall.SOUTH.value] = sprite

    def corner_wall_chooser(self, sprites: list[Any],
                            is_top: bool, is_bottom: bool,
                            is_left: bool, is_right: bool) -> None:

        if is_top and is_left:
            sprite = self.maze_sprites["wall_double_outer_corner_top_left"]
        elif is_left:
            sprite = self.maze_sprites["wall_double_t_junction_top_left"]
        elif is_top:
            sprite = self.maze_sprites["wall_top_join_left"]
        else:
            sprite = self.maze_sprites["wall_curve_large_top_left"]
        sprites[CornerWall.NORTH_WEST.value] = sprite

        if is_top and is_right:
            sprite = self.maze_sprites["wall_double_outer_corner_top_right"]
        elif is_right:
            sprite = self.maze_sprites["wall_double_t_junction_top_right"]
        elif is_top:
            sprite = self.maze_sprites["wall_top_join_right"]
        else:
            sprite = self.maze_sprites["wall_curve_large_top_right"]
        sprites[CornerWall.NORTH_EAST.value] = sprite

        if is_left and is_bottom:
            sprite = self.maze_sprites["wall_double_outer_corner_bottom_left"]
        elif is_bottom:
            sprite = self.maze_sprites[
                "wall_double_t_junction_bottom_top_right"]
        elif is_left:
            sprite = self.maze_sprites["wall_double_t_junction_bottom_left"]
        else:
            sprite = self.maze_sprites["wall_curve_large_bottom_left"]
        sprites[CornerWall.SOUTH_WEST.value] = sprite

        if is_bottom and is_right:
            sprite = self.maze_sprites["wall_double_outer_corner_bottom_right"]
        elif is_bottom:
            sprite = self.maze_sprites[
                "wall_double_t_junction_bottom_top_left"]
        elif is_right:
            sprite = self.maze_sprites["wall_double_t_junction_bottom_right"]
        else:
            sprite = self.maze_sprites["wall_curve_large_bottom_right"]
        sprites[CornerWall.SOUTH_EAST.value] = sprite

    def sprites_chooser(self, x: int, y: int) -> list[SpriteData]:
        sprites = [self.maze_sprites["empty_tile"] for _ in range(15)]

        is_top = y == 0
        is_bottom = y == len(self.maze_grid) - 1
        is_left = x == 0
        is_right = x == len(self.maze_grid[0]) - 1

        self.straight_wall_chooser(
            sprites, is_top, is_bottom, is_left, is_right)
        self.corner_wall_chooser(
            sprites, is_top, is_bottom, is_left, is_right)

        return sprites

    def need_little_corner(self, current_square: int, next_square: int,
                           avoid_wall: list[int],
                           mandatory_wall: list[int],
                           corner_value: int) -> int:

        if current_square & avoid_wall[0] or current_square & avoid_wall[1]:
            return 0
        if (not (next_square & mandatory_wall[0])
                and not (next_square & mandatory_wall[1])):
            return 0
        return corner_value

    def need_little_corners(self, x: int, y: int, corner: CornerWall) -> int:
        is_top = y == 0
        is_bottom = y == len(self.maze_grid) - 1
        is_left = x == 0
        is_right = x == len(self.maze_grid[0]) - 1

        if (corner.value == CornerWall.NORTH_EAST.value
                and not is_right
                and not is_top):
            return self.need_little_corner(self.maze_grid[y][x],
                                           self.maze_grid[y - 1][x + 1],
                                           [Wall.EAST.value, Wall.NORTH.value],
                                           [Wall.SOUTH.value, Wall.WEST.value],
                                           corner.value)

        elif (corner.value == CornerWall.NORTH_WEST.value
              and not is_left
              and not is_top):
            return self.need_little_corner(self.maze_grid[y][x],
                                           self.maze_grid[y - 1][x - 1],
                                           [Wall.WEST.value, Wall.NORTH.value],
                                           [Wall.SOUTH.value, Wall.EAST.value],
                                           corner.value)

        elif (corner.value == CornerWall.SOUTH_EAST.value
              and not is_right
              and not is_bottom):
            return self.need_little_corner(self.maze_grid[y][x],
                                           self.maze_grid[y + 1][x + 1],
                                           [Wall.EAST.value, Wall.SOUTH.value],
                                           [Wall.NORTH.value, Wall.WEST.value],
                                           corner.value)

        elif (corner.value == CornerWall.SOUTH_WEST.value
                and not is_left
                and not is_bottom):
            return self.need_little_corner(self.maze_grid[y][x],
                                           self.maze_grid[y + 1][x - 1],
                                           [Wall.WEST.value, Wall.SOUTH.value],
                                           [Wall.NORTH.value, Wall.EAST.value],
                                           corner.value)
        return 0

    def little_corner_handle(self, corner_value: int) -> SpriteData:
        if corner_value == CornerWall.NORTH_EAST.value:
            return self.maze_sprites["wall_small_corner_bottom_left"]

        if corner_value == CornerWall.NORTH_WEST.value:
            return self.maze_sprites["wall_small_corner_bottom_right"]

        if corner_value == CornerWall.SOUTH_EAST.value:
            return self.maze_sprites["wall_small_corner_top_left"]

        return self.maze_sprites["wall_small_corner_top_right"]

    def handle_corner(self, w1: int, w2: int,
                      sprites: list[SpriteData], y: int, x: int,
                      corner: CornerWall) -> SpriteData:
        corner_needed = self.need_little_corners(x, y, corner)
        if corner_needed > 0:
            return self.little_corner_handle(corner_needed)
        if w1 and w2:
            return sprites[w1 + w2]
        if w1 and not w2:
            return sprites[w1]
        if w2 and not w1:
            return sprites[w2]
        return sprites[0]

    def sprite_filler(self, x: int, y: int) -> list[list[SpriteData]]:
        n = self.maze_grid[y][x] & Wall.NORTH.value
        e = self.maze_grid[y][x] & Wall.EAST.value
        s = self.maze_grid[y][x] & Wall.SOUTH.value
        w = self.maze_grid[y][x] & Wall.WEST.value

        sprites: list[SpriteData] = self.sprites_chooser(x, y)

        north_west_sprite = self.handle_corner(w, n, sprites,
                                               y, x, CornerWall.NORTH_WEST)
        north_sprite = sprites[n]
        north_east_sprite = self.handle_corner(n, e, sprites,
                                               y, x, CornerWall.NORTH_EAST)

        west_sprite = sprites[w]
        empty_sprite = sprites[0]
        east_sprite = sprites[e]

        south_west_sprite = self.handle_corner(w, s, sprites,
                                               y, x, CornerWall.SOUTH_WEST)
        south_sprite = sprites[s]
        sout_east_sprite = self.handle_corner(s, e, sprites,
                                              y, x, CornerWall.SOUTH_EAST)
        return [
                [north_west_sprite, north_sprite, north_east_sprite],
                [west_sprite, empty_sprite, east_sprite],
                [south_west_sprite, south_sprite, sout_east_sprite]
                ]

    def put_tile_in_image(self, tile: list[list[SpriteData]],
                          x: int, y: int, dest_img_buffer: ndarray,
                          dest_img_width: int) -> None:

        tile_x_start = self.x_start + int(x * self.tile_size)
        tile_y_start = self.y_start + int(y * self.tile_size)

        for tile_y in range(3):
            sub_y_start = tile_y_start + tile_y * self.sprite_size
            for tile_x in range(3):
                sub_x_start = tile_x_start + tile_x * self.sprite_size
                sub_w = self.sprite_size
                sub_h = self.sprite_size
                self.put_sprite_in_image(dest_img_buffer, dest_img_width,
                                         sub_x_start, sub_y_start,
                                         sub_w, sub_h,
                                         tile[tile_y][tile_x])

    def render(self, dest_img_buffer: ndarray,
               dest_img_width: int,
               game_board: GameBoard,
               window: pygame.Surface) -> None:

        for y in range(len(self.maze_grid)):
            for x in range(len(self.maze_grid[y])):
                tile = self.sprite_filler(x, y)
                self.put_tile_in_image(tile, x, y,
                                       dest_img_buffer,
                                       dest_img_width)
