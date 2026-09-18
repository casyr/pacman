from . import SpriteSheetManager
from .graphics import Graphics
from pygame import Surface
from .sprite_model import SpriteModel
from enum import Enum


class Wall(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


class Corner(Enum):
    NORTH_WEST = Wall.NORTH.value + Wall.WEST.value
    NORTH_EAST = Wall.NORTH.value + Wall.EAST.value
    SOUTH_EAST = Wall.SOUTH.value + Wall.EAST.value
    SOUTH_WEST = Wall.SOUTH.value + Wall.WEST.value


class MazeRenderer:

    def __init__(self, maze_sprites: SpriteSheetManager):
        self.maze_sprites = maze_sprites

    def sprite_chooser(self, x: int, y: int, maze_sprites: SpriteSheetManager,
                       maze: list[list[int]]) -> list[SpriteModel]:

        get_sprite = maze_sprites.get_sprite

        sprites = [get_sprite("empty_tile"),
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        if x == 0:
            sprites[Wall.WEST.value] = get_sprite("wall_double_vertical_left")
        else:
            sprites[Wall.WEST.value] = get_sprite("wall_single_vertical_left")

        if x == len(maze[0]) - 1:
            sprites[Wall.EAST.value] = get_sprite("wall_double_vertical_right")
        else:
            sprites[Wall.EAST.value] = get_sprite("wall_single_vertical_right")

        if y == 0:
            sprites[Wall.NORTH.value] = get_sprite("wall_double_horizontal_top")
        else:
            sprites[Wall.NORTH.value] = get_sprite("wall_single_horizontal_top")

        if y == len(maze) - 1:
            sprites[Wall.SOUTH.value] = get_sprite("wall_double_horizontal_bottom")
        else:
            sprites[Wall.SOUTH.value] = get_sprite("wall_single_horizontal_bottom")

        if y == 0 and x == 0:
            sprites[Corner.NORTH_WEST.value] = get_sprite("wall_double_outer_corner_top_left")
        elif x == 0:
            sprites[Corner.NORTH_WEST.value] = get_sprite("wall_double_t_junction_top_left")
        elif y == 0:
            sprites[Corner.NORTH_WEST.value] = get_sprite("wall_top_join_left")
        else:
            sprites[Corner.NORTH_WEST.value] = get_sprite("wall_curve_large_top_left")

        if y == 0 and x == len(maze[0]) - 1:
            sprites[Corner.NORTH_EAST.value] = get_sprite("wall_double_outer_corner_top_right")
        elif x == len(maze[0]) - 1:
            sprites[Corner.NORTH_EAST.value] = get_sprite("wall_double_t_junction_top_right")
        elif y == 0:
            sprites[Corner.NORTH_EAST.value] = get_sprite("wall_top_join_right")
        else:
            sprites[Corner.NORTH_EAST.value] = get_sprite("wall_curve_large_top_right")

        if x == 0 and y == len(maze) - 1:
            sprites[Corner.SOUTH_WEST.value] = get_sprite("wall_double_outer_corner_bottom_left")
        elif y == len(maze) - 1:
            sprites[Corner.SOUTH_WEST.value] = get_sprite("wall_double_t_junction_bottom_top_right")
        elif x == 0:
            sprites[Corner.SOUTH_WEST.value] = get_sprite("wall_double_t_junction_bottom_left")
        else:
            sprites[Corner.SOUTH_WEST.value] = get_sprite("wall_curve_large_bottom_left")

        if (y == len(maze) - 1) and (x == len(maze[0]) - 1):
            sprites[Corner.SOUTH_EAST.value] = get_sprite("wall_double_outer_corner_bottom_right")
        elif y == len(maze) - 1:
            sprites[Corner.SOUTH_EAST.value] = get_sprite("wall_double_t_junction_bottom_top_left")
        elif x == len(maze[0]) - 1:
            sprites[Corner.SOUTH_EAST.value] = get_sprite("wall_double_t_junction_bottom_right")
        else:
            sprites[Corner.SOUTH_EAST.value] = get_sprite("wall_curve_large_bottom_right")

        return sprites

    def need_little_corners_(self, maze: list[list[int]], x: int, y: int,
                           corner: Corner) -> int:

        is_top = y == 0
        is_bottom = y == len(maze) - 1
        is_left = x == 0
        is_right = x == len(maze[0]) - 1

        if not is_top and not is_right and not maze[y][x] & Wall.EAST.value and not maze[y][x] & Wall.NORTH.value and corner.value == Corner.NORTH_EAST.value and (maze[y - 1][x + 1] & 4 or maze[y - 1][x + 1] & 8):
            return Corner.NORTH_EAST.value

        if not is_top and not is_left and not maze[y][x] & Wall.WEST.value and not maze[y][x] & Wall.NORTH.value and corner.value == Corner.NORTH_WEST.value and (maze[y - 1][x - 1] & 4 or maze[y - 1][x - 1] & 2):
            return Corner.NORTH_WEST.value

        if not is_bottom and not is_right and not maze[y][x] & Wall.EAST.value and not maze[y][x] & Wall.SOUTH.value and corner.value == Corner.SOUTH_EAST.value and (maze[y + 1][x + 1] & 1 or maze[y + 1][x + 1] & 8):
            return Corner.SOUTH_EAST.value

        if not is_left and not is_bottom and not maze[y][x] & Wall.WEST.value and not maze[y][x] & Wall.SOUTH.value and corner.value == Corner.SOUTH_WEST.value and (maze[y + 1][x - 1] & 1 or maze[y + 1][x - 1] & 2):
            return Corner.SOUTH_WEST.value

        return 0

    def need_little_corner(self, current_square: int, next_square: int,
                           avoid_wall: list[int],
                           mandatory_wall: list[int],
                           corner_value: int) -> int:

        if current_square & avoid_wall[0] or current_square & avoid_wall[1]:
            return 0
        if (not next_square & mandatory_wall[0] or not
                next_square & mandatory_wall[1]):
            return 0
        return corner_value

    def need_little_corners(self, maze: list[list[int]], x: int, y: int,
                            corner: Corner) -> int:

        is_top = y == 0
        is_bottom = y == len(maze) - 1
        is_left = x == 0
        is_right = x == len(maze[0]) - 1

        if (corner.value == Corner.NORTH_EAST.value
                and not is_right
                and not is_top):
            return self.need_little_corner(maze[y][x], maze[y - 1][x + 1],
                                           [Wall.EAST.value, Wall.NORTH.value],
                                           [Wall.SOUTH.value, Wall.WEST.value],
                                           Corner.NORTH_EAST.value)

        elif (corner.value == Corner.NORTH_WEST.value
              and not is_left
              and not is_top):
            return self.need_little_corner(maze[y][x], maze[y - 1][x - 1],
                                           [Wall.WEST.value, Wall.NORTH.value],
                                           [Wall.NORTH.value, Wall.WEST.value],
                                           corner.value)

        elif (corner.value == Corner.SOUTH_EAST.value
              and not is_right
              and not is_bottom):
            return self.need_little_corner(maze[y][x], maze[y + 1][x - 1],
                                           [Wall.WEST.value, Wall.SOUTH.value],
                                           [Wall.NORTH.value, Wall.EAST.value],
                                           corner.value)

        elif not is_left and not is_bottom:
            return self.need_little_corner(maze[y][x], maze[y + 1][x - 1],
                                           [Wall.EAST.value, Wall.NORTH.value],
                                           [Wall.NORTH.value, Wall.EAST.value],
                                           corner.value)
        return 0

    def little_corner_handle(self, corner_value: int) -> SpriteModel:
        if corner_value == Corner.NORTH_EAST.value:
            return (self.maze_sprites.get_sprite("wall_small_corner_bottom_left"))

        if corner_value == Corner.NORTH_WEST.value:
            return (self.maze_sprites.get_sprite("wall_small_corner_bottom_right"))

        if corner_value == Corner.SOUTH_EAST.value:
            return (self.maze_sprites.get_sprite("wall_small_corner_top_left"))

        return (self.maze_sprites.get_sprite("wall_small_corner_top_right"))

    def handle_corner(self, w1: int, w2: int,
                      sprites: list[SpriteModel],
                      maze: list[list[int]], y: int, x: int,
                      corner: Corner) -> SpriteModel:
        corner_needed = self.need_little_corners(maze, x, y, corner)
        if corner_needed > 0:
            return self.little_corner_handle(corner_needed)
        if w1 and w2:
            return sprites[w1 + w2]
        if w1 and not w2:
            return sprites[w1]
        if w2 and not w1:
            return sprites[w2]
        return sprites[0]

    def sprite_filler(self, maze: list[list[int]],
                      x: int, y: int, maze_sprites: SpriteSheetManager
                      ) -> list[list[SpriteModel]]:

        n = maze[y][x] & Wall.NORTH.value  
        e = maze[y][x] & Wall.EAST.value
        s = maze[y][x] & Wall.SOUTH.value
        w = maze[y][x] & Wall.WEST.value

        sprites: list[SpriteModel] = self.sprite_chooser(x, y,
                                                         maze_sprites, maze)

        north_west_sprite = self.handle_corner(w, n, sprites, maze,
                                               y, x, Corner.NORTH_WEST)
        north_sprite = sprites[n]
        north_east_sprite = self.handle_corner(n, e, sprites, maze,
                                               y, x, Corner.NORTH_EAST)

        west_sprite = sprites[w]
        empty_sprite = sprites[0]
        east_sprite = sprites[e]

        south_west_sprite = self.handle_corner(w, s, sprites, maze,
                                               y, x, Corner.SOUTH_WEST)
        south_sprite = sprites[s]
        sout_east_sprite = self.handle_corner(s, e, sprites, maze,
                                              y, x, Corner.SOUTH_EAST)
        return [
                [north_west_sprite, north_sprite, north_east_sprite],
                [west_sprite, empty_sprite, east_sprite],
                [south_west_sprite, south_sprite, sout_east_sprite]
                ]

    def put_tile_in_image(self, img: Surface, tile: list[list[SpriteModel]],
                          maze_width: int, maze_height: int, x: int, y: int,
                          img_width: int, img_height: int):

        tile_width_and_length = 24 * 3
        sprite_width_and_length = 8 * 3
        graphic = Graphics()

        half_img_width = img_width // 2
        half_img_height = img_height // 2

        x_dest = half_img_width - ((maze_width // 2) * tile_width_and_length)
        y_dest = half_img_height - ((maze_height // 2) * tile_width_and_length)

        for tile_y in range(3):
            for tile_x in range(3):
                x_gap = (tile_x * sprite_width_and_length)
                y_gap = (tile_y * sprite_width_and_length)
                dest_x = x_dest + x * tile_width_and_length + x_gap
                dest_y = y_dest + y * tile_width_and_length + y_gap
                graphic.put_sprite_in_image(img, dest_x, dest_y,
                                            tile[tile_y][tile_x])

    def render_in_img(self, maze: list[list[int]],
                      maze_width: int, maze_height: int,
                      maze_sprites: SpriteSheetManager) -> Surface:

        img_width = 1900
        img_height = 1900
        graphic = Graphics()
        img = graphic.new_image(img_width, img_height)

        for y in range(len(maze)):
            for x in range(len(maze[y])):
                tile = self.sprite_filler(maze, x, y, maze_sprites)
                self.put_tile_in_image(img, tile, maze_width, maze_height,
                                       x, y, img_width, img_height)

        return (img)
