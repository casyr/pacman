from . import SpriteSheetManager
from mazegenerator import MazeGenerator
from .graphics import Graphics
from pygame import Surface
from .sprite_model import SpriteModel


class MazeRenderer:

    def sprite_chooser(self, maze: list[list[int]], x: int, y: int,
                       maze_sprites: SpriteSheetManager
                       ) -> list[list[SpriteModel]]:

        tile_sprite_lits: list[list[SpriteModel]] = [[], [], []]

        if x == 0 and y == 0:
            sprite = maze_sprites.get_sprite("wall_double_outer_corner_top_left")
            tile_sprite_lits[0].append(sprite)

        if y == 0:
            sprite = maze_sprites.get_sprite("wall_double_horizontal_top")
            tile_sprite_lits[0].append(sprite)

        if x == len(maze[0]) - 1 and y == 0:
            sprite = maze_sprites.get_sprite("wall_double_outer_corner_top_right")
            tile_sprite_lits[0].append(sprite)

        if x == 0:
            sprite = maze_sprites.get_sprite("wall_double_vertical_left")
            tile_sprite_lits[1].append(sprite)

        if x == len(maze[0]) - 1:
            sprite = maze_sprites.get_sprite("wall_double_vertical_right")
            tile_sprite_lits[1].append(sprite)

        if x == 0 and y == len(maze) - 1:
            sprite = maze_sprites.get_sprite("wall_double_outer_corner_bottom_left")
            tile_sprite_lits[1].append(sprite)

        if x == len(maze[0]) - 1 and y == len(maze) - 1:
            sprite = maze_sprites.get_sprite("wall_double_outer_corner_bottom_right")
            tile_sprite_lits[y].append(sprite)



        if x == len(maze[0]) - 1:
            sprite = maze_sprites.get_sprite("wall_double_vertical_right")
            tile_sprite_lits[y].append(sprite)



        if y == len(maze) - 1:
            sprite = maze_sprites.get_sprite("wall_double_horizontal_bottom")
            tile_sprite_lits[y].append(sprite)

        if maze[y][x] & 8 and maze[y][x] & 1:
            sprite = maze_sprites.get_sprite("wall_curve_large_top_left")
            tile_sprite_lits[0][1] = sprite

        if maze[y][x] & 1 and maze[y][x] & 2:
            sprite = maze_sprites.get_sprite("wall_curve_large_top_right")
            tile_sprite_lits[y].append(sprite)

        if maze[y][x] & 1 and maze[y][x] & 2 == 0:
            sprite = maze_sprites.get_sprite("wall_single_horizontal_top")
            tile_sprite_lits[y].append(sprite)

        if maze[y][x] & 2 and maze[y][x] & 4:
            sprite = maze_sprites.get_sprite("wall_curve_large_bottom_right")
            tile_sprite_lits[y].append(sprite)

        if maze[y][x] & 2 and maze[y][x] & 4 == 0:
            sprite = maze_sprites.get_sprite("wall_single_vertical_right")
            tile_sprite_lits[y].append(sprite)

        if maze[y][x] & 4 and maze[y][x] & 8:
            sprite = maze_sprites.get_sprite("wall_curve_large_bottom_left")
            tile_sprite_lits[y].append(sprite)

        if maze[y][x] & 4 and maze[y][x] & 8 != 0:
            sprite = maze_sprites.get_sprite("wall_single_horizontal_bottom")
            tile_sprite_lits[y].append(sprite)

        if maze[y][x] & 8 and maze[y][x] & 1 == 0:
            sprite = maze_sprites.get_sprite("wall_single_vertical_left")
            tile_sprite_lits[y].append(sprite)

        else:
            sprite = maze_sprites.get_sprite("empty_tile")
            tile_sprite_lits[y].append(sprite)
        return (tile_sprite_lits)

    def put_tile_in_image(self, tile: list[list[SpriteModel]], maze_width: int,
                          maze_height: int, x: int, y: int):

        graphic = Graphics()

        img_width = 1900
        img_height = 1900

        img = graphic.new_image(img_width, img_height)

        tile_width_and_length = 24
        sprite_width_and_length = 8

        x_dest = (img_width // 2) - ((maze_width // 2) * tile_width_and_length)
        y_dest = (img_height // 2) - ((maze_height // 2) * tile_width_and_length)

        print(len(tile[0]))
        print(len(tile[1]))
        print(len(tile[2]))
        for tile_y in range(3):
            for tile_x in range(3):
                dest_x = x_dest + x * tile_width_and_length + (tile_x * sprite_width_and_length)
                dest_y = y_dest + y * tile_width_and_length + (tile_y * sprite_width_and_length)
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

        for y in range(len(maze)):
            for x in range(len(maze[y])):
                tile = self.sprite_chooser(maze, x, y, maze_sprites)
                self.put_tile_in_image(tile, maze_width, maze_height, x, y)

        return (img)
