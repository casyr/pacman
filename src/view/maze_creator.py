from . import SpriteSheetManager
from mazegenerator import MazeGenerator
from .graphics import Graphics
from pygame import Surface
from .sprite_model import SpriteModel
from enum import Enum


class Wall(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

class MazeRenderer:

    def sprite_chooser(self, x: int, y: int, maze_sprites: SpriteSheetManager,
                       maze: list[list[int]]) -> dict[int, SpriteModel]:

        sprites = {}

        sprites[0] = maze_sprites.get_sprite("empty_tile")

        if x == 0:
            sprites[Wall.WEST.value] = maze_sprites.get_sprite("wall_double_vertical_left")
        else:
            sprites[Wall.WEST.value] = maze_sprites.get_sprite("wall_single_vertical_left")

        if x == len(maze[0]) - 1:
            sprites[Wall.EAST.value] = maze_sprites.get_sprite("wall_double_vertical_right")
        else:
            sprites[Wall.EAST.value] = maze_sprites.get_sprite("wall_single_vertical_right")

        if y == 0:
            sprites[Wall.NORTH.value] = maze_sprites.get_sprite("wall_double_horizontal_top")
        else:
            sprites[Wall.NORTH.value] = maze_sprites.get_sprite("wall_single_horizontal_top")

        if y == len(maze) - 1:
            sprites[Wall.SOUTH.value] = maze_sprites.get_sprite("wall_double_horizontal_bottom")
        else:
            sprites[Wall.SOUTH.value] = maze_sprites.get_sprite("wall_single_horizontal_bottom")

        if y == 0 and x == 0:
            sprites[Wall.WEST.value + Wall.NORTH.value] = maze_sprites.get_sprite("wall_double_outer_corner_top_left")
        else:
            sprites[Wall.WEST.value + Wall.NORTH.value] = maze_sprites.get_sprite("wall_single_corner_top_left")

        if y == 0 and x == len(maze[0]) - 1:
            sprites[Wall.EAST.value + Wall.NORTH.value] = maze_sprites.get_sprite("wall_double_outer_corner_top_right")
        else:
            sprites[Wall.EAST.value + Wall.NORTH.value] = maze_sprites.get_sprite("wall_single_corner_top_right")

        if x == 0 and y == len(maze) - 1:
            sprites[Wall.SOUTH.value + Wall.WEST.value] = maze_sprites.get_sprite("wall_double_outer_corner_bottom_left")
        else:
            sprites[Wall.SOUTH.value + Wall.WEST.value] = maze_sprites.get_sprite("wall_single_corner_bottom_left")

        if y == len(maze) - 1 and x == len(maze[0]) - 1:
            sprites[Wall.SOUTH.value + Wall.EAST.value] = maze_sprites.get_sprite("wall_double_outer_corner_bottom_right")
        else:
            sprites[Wall.SOUTH.value + Wall.EAST.value] = maze_sprites.get_sprite("wall_single_corner_bottom_right")

        print(sprites)
        return sprites

    def handle_corner(self, w1: int, w2: int,
                      sprites: dict[int, SpriteModel]) -> SpriteModel:
        if w1 and w2:
            return sprites[w1 + w2]
        if w1 and not w2:
            return sprites[w1]
        if w2 and not w1:
            return sprites[w2]
        return sprites[0]

    def sprite_filler(self, maze: list[list[int]],
                      x: int, y: int, maze_sprites: SpriteSheetManager
                        )-> list[list[SpriteModel]]:

        n = maze[y][x] & Wall.NORTH.value
        e = maze[y][x] & Wall.EAST.value
        s = maze[y][x] & Wall.SOUTH.value
        w = maze[y][x] & Wall.WEST.value

        sprites: dict[int, SpriteModel] = self.sprite_chooser(x, y, maze_sprites, maze)
        print(x, y, "\n",
              f"    {n}    \n",
              f"{w}      {e} \n",
              f"    {s}    \n",)
        list_ = [
                [self.handle_corner(w, n, sprites), sprites[n], self.handle_corner(n, e, sprites)],
                [sprites[w], sprites[0], sprites[e]],
                [self.handle_corner(w, s, sprites), sprites[s], self.handle_corner(s, e, sprites)]
                ]
        names = [sprite.sprite_name for row in list_ for sprite in row]
        print(names, "\n")
        return [
                [self.handle_corner(w, n, sprites), sprites[n], self.handle_corner(n, e, sprites)],
                [sprites[w], sprites[0], sprites[e]],
                [self.handle_corner(w, s, sprites), sprites[s], self.handle_corner(s, e, sprites)]
                ]

    def put_tile_in_image(self, img: Surface, tile: list[list[SpriteModel]], maze_width: int,
                          maze_height: int, x: int, y: int, img_width: int, img_height: int):

        tile_width_and_length = 24 * 3
        sprite_width_and_length = 8 * 3
        graphic = Graphics()
        x_dest = (img_width // 2) - ((maze_width // 2) * tile_width_and_length)
        y_dest = (img_height // 2) - ((maze_height // 2) * tile_width_and_length)

        for tile_y in range(3):
            for tile_x in range(3):
                dest_x = x_dest + x * tile_width_and_length + (tile_x * sprite_width_and_length)
                dest_y = y_dest + y * tile_width_and_length + (tile_y * sprite_width_and_length)
                print( dest_x," ", dest_y," " ,tile[tile_y][tile_x].sprite_name)
                graphic.put_sprite_in_image(img, dest_x, dest_y, tile[tile_y][tile_x])

    def render_in_img(self) -> Surface:

        maze_width = 15
        maze_height = 15
        maze_generator = MazeGenerator(
            (maze_width, maze_height),
            False,
            (0, 0),
            (14, 14),
        )

        maze_generator.generate()
        maze = maze_generator.maze

        maze_sprites = SpriteSheetManager("sprites/maze_sprites/maze_sprites.bmp",
                                          "sprites/maze_sprites/maze_sprites.yaml")
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
