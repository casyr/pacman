from . import SpriteSheetManager
from .graphic import Graphic
from pygame import Surface
from .sprite_model import SpriteModel
from enum import Enum
from typing import Any
from numpy import ndarray


class Wall(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


class CornerWall(Enum):
    NORTH_WEST = Wall.NORTH.value + Wall.WEST.value
    NORTH_EAST = Wall.NORTH.value + Wall.EAST.value
    SOUTH_EAST = Wall.SOUTH.value + Wall.EAST.value
    SOUTH_WEST = Wall.SOUTH.value + Wall.WEST.value


class MazeRenderer:

    def __init__(self, maze_sprites: SpriteSheetManager,
                 maze: list[list[int]], maze_width: int, maze_height: int,
                 screen_width: int, screen_height: int):
        self.maze_sprites = maze_sprites
        self.graphic = Graphic()
        self.scaling = self.graphic.get_scaling(maze_width, maze_height,
                                                screen_width, screen_height)
        self.maze = maze
        self.maze_width = maze_width
        self.maze_height = maze_height

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.tile_size = self.graphic.get_tile_size(self.maze_width, self.maze_height, self.screen_width, self.screen_height)
        self.sprite_size = self.tile_size // 3

    def straight_wall_chooser(self, sprites: list[Any],
                              is_top: bool, is_bottom: bool,
                              is_left: bool, is_right: bool) -> None:
        if is_left:
            sprite = self.maze_sprites.get_sprite("wall_double_vertical_left")
        else:
            sprite = self.maze_sprites.get_sprite("wall_single_vertical_left")
        sprites[Wall.WEST.value] = sprite

        if is_right:
            sprite = self.maze_sprites.get_sprite("wall_double_vertical_right")
        else:
            sprite = self.maze_sprites.get_sprite("wall_single_vertical_right")
        sprites[Wall.EAST.value] = sprite

        if is_top:
            sprite = self.maze_sprites.get_sprite("wall_double_horizontal_top")
        else:
            sprite = self.maze_sprites.get_sprite("wall_single_horizontal_top")
        sprites[Wall.NORTH.value] = sprite

        if is_bottom:
            sprite = self.maze_sprites.get_sprite("wall_double_horizontal_"
                                                  "bottom")
        else:
            sprite = self.maze_sprites.get_sprite("wall_single_horizontal_"
                                                  "bottom")
        sprites[Wall.SOUTH.value] = sprite

    def corner_wall_chooser(self, sprites: list[Any],
                            is_top: bool, is_bottom: bool,
                            is_left: bool, is_right: bool) -> None:

        get_sprite = self.maze_sprites.get_sprite

        if is_top and is_left:
            sprite = get_sprite("wall_double_outer_corner_top_left")
        elif is_left:
            sprite = get_sprite("wall_double_t_junction_top_left")
        elif is_top:
            sprite = get_sprite("wall_top_join_left")
        else:
            sprite = get_sprite("wall_curve_large_top_left")
        sprites[CornerWall.NORTH_WEST.value] = sprite

        if is_top and is_right:
            sprite = get_sprite("wall_double_outer_corner_top_right")
        elif is_right:
            sprite = get_sprite("wall_double_t_junction_top_right")
        elif is_top:
            sprite = get_sprite("wall_top_join_right")
        else:
            sprite = get_sprite("wall_curve_large_top_right")
        sprites[CornerWall.NORTH_EAST.value] = sprite

        if is_left and is_bottom:
            sprite = get_sprite("wall_double_outer_corner_bottom_left")
        elif is_bottom:
            sprite = get_sprite("wall_double_t_junction_bottom_top_right")
        elif is_left:
            sprite = get_sprite("wall_double_t_junction_bottom_left")
        else:
            sprite = get_sprite("wall_curve_large_bottom_left")
        sprites[CornerWall.SOUTH_WEST.value] = sprite

        if (is_bottom) and (is_right):
            sprite = get_sprite("wall_double_outer_corner_bottom_right")
        elif is_bottom:
            sprite = get_sprite("wall_double_t_junction_bottom_top_left")
        elif is_right:
            sprite = get_sprite("wall_double_t_junction_bottom_right")
        else:
            sprite = get_sprite("wall_curve_large_bottom_right")
        sprites[CornerWall.SOUTH_EAST.value] = sprite

    def sprites_chooser(self, x: int, y: int) -> list[SpriteModel]:

        sprites = [self.maze_sprites.get_sprite("empty_tile")
                   for _ in range(15)]

        is_top = y == 0
        is_bottom = y == len(self.maze) - 1
        is_left = x == 0
        is_right = x == len(self.maze[0]) - 1

        self.straight_wall_chooser(sprites, is_top, is_bottom, is_left,
                                   is_right)

        self.corner_wall_chooser(sprites, is_top, is_bottom, is_left,
                                 is_right)

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

    def need_little_corners(self, x: int, y: int,
                            corner: CornerWall) -> int:

        is_top = y == 0
        is_bottom = y == len(self.maze) - 1
        is_left = x == 0
        is_right = x == len(self.maze[0]) - 1

        if (corner.value == CornerWall.NORTH_EAST.value
                and not is_right
                and not is_top):
            return self.need_little_corner(self.maze[y][x],
                                           self.maze[y - 1][x + 1],
                                           [Wall.EAST.value, Wall.NORTH.value],
                                           [Wall.SOUTH.value, Wall.WEST.value],
                                           corner.value)

        elif (corner.value == CornerWall.NORTH_WEST.value
              and not is_left
              and not is_top):
            return self.need_little_corner(self.maze[y][x],
                                           self.maze[y - 1][x - 1],
                                           [Wall.WEST.value, Wall.NORTH.value],
                                           [Wall.SOUTH.value, Wall.EAST.value],
                                           corner.value)

        elif (corner.value == CornerWall.SOUTH_EAST.value
              and not is_right
              and not is_bottom):
            return self.need_little_corner(self.maze[y][x],
                                           self.maze[y + 1][x + 1],
                                           [Wall.EAST.value, Wall.SOUTH.value],
                                           [Wall.NORTH.value, Wall.WEST.value],
                                           corner.value)

        elif (corner.value == CornerWall.SOUTH_WEST.value
                and not is_left
                and not is_bottom):
            return self.need_little_corner(self.maze[y][x],
                                           self.maze[y + 1][x - 1],
                                           [Wall.WEST.value, Wall.SOUTH.value],
                                           [Wall.NORTH.value, Wall.EAST.value],
                                           corner.value)
        return 0

    def little_corner_handle(self, corner_value: int) -> SpriteModel:

        get_sprite = self.maze_sprites.get_sprite

        if corner_value == CornerWall.NORTH_EAST.value:
            return (get_sprite("wall_small_corner_bottom_left"))

        if corner_value == CornerWall.NORTH_WEST.value:
            return (get_sprite("wall_small_corner_bottom_right"))

        if corner_value == CornerWall.SOUTH_EAST.value:
            return (get_sprite("wall_small_corner_top_left"))

        return (get_sprite("wall_small_corner_top_right"))

    def handle_corner(self, w1: int, w2: int,
                      sprites: list[SpriteModel], y: int, x: int,
                      corner: CornerWall) -> SpriteModel:
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

    def sprite_filler(self, x: int, y: int) -> list[list[SpriteModel]]:

        n = self.maze[y][x] & Wall.NORTH.value
        e = self.maze[y][x] & Wall.EAST.value
        s = self.maze[y][x] & Wall.SOUTH.value
        w = self.maze[y][x] & Wall.WEST.value

        sprites: list[SpriteModel] = self.sprites_chooser(x, y)

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

    def put_tile_in_image(self, img: Surface,
                          tile: list[list[SpriteModel]],
                          x: int, y: int) -> None:

        usable_width = self.graphic.get_usable_width(self.screen_width)
        usable_height = self.graphic.get_usable_height(self.screen_height)
        half_img_width = usable_width // 2 + self.graphic.get_padding() // 2
        half_img_height = usable_height // 2 + self.graphic.get_padding() // 2

        x_dest = half_img_width - ((self.maze_width // 2) * self.tile_size)
        y_dest = half_img_height - ((self.maze_height // 2) * self.tile_size)

        for tile_y in range(3):
            for tile_x in range(3):
                x_gap = (tile_x * self.sprite_size)
                y_gap = (tile_y * self.sprite_size)
                dest_x = x_dest + x * self.tile_size + x_gap
                dest_y = y_dest + y * self.tile_size + y_gap
                self.graphic.put_sprite_in_image_(img, dest_x, dest_y,
                                                 tile[tile_y][tile_x],
                                                 self.maze_width, self.maze_height)

    def put_tile_in_image_(self, tile: list[list[SpriteModel]],
                           x: int, y: int, dest_img_buffer: ndarray,
                           dest_img_size: int) -> None:
        usable_width = self.graphic.get_usable_width(self.screen_width)
        usable_height = self.graphic.get_usable_height(self.screen_height)
        half_img_width = usable_width // 2 + self.graphic.get_padding() // 2
        half_img_height = usable_height // 2 + self.graphic.get_padding() // 2

        x_dest = half_img_width - ((self.maze_width // 2) * self.tile_size)
        y_dest = half_img_height - ((self.maze_height // 2) * self.tile_size)

        for tile_y in range(3):
            for tile_x in range(3):
                x_gap = (tile_x * self.sprite_size)
                y_gap = (tile_y * self.sprite_size)
                dest_x = x_dest + x * self.tile_size + x_gap
                dest_y = y_dest + y * self.tile_size + y_gap
                self.graphic.put_sprite_in_image_(dest_img_buffer,
                                                  dest_img_size,
                                                  dest_x, dest_y,
                                                  tile[tile_y][tile_x],
                                                  self.maze_width,
                                                  self.maze_height)

    def render_in_img(self, dest_img_buffer: ndarray,
                      dest_img_size: int) -> None:

        print("render")
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                tile = self.sprite_filler(x, y)
                self.put_tile_in_image_(tile, x, y,
                                        dest_img_buffer,
                                        dest_img_size)
        print("end render")
