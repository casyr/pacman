from . import SpriteSheetManager
from mazegenerator import MazeGenerator
from .graphics import Graphics


class MazeRenderer:

    def render_in_img(self) -> pygame.Surface:

        maze_width = 21
        maze_height = 21
        maze_generator = MazeGenerator(
            (maze_width, maze_height),
            False,
            (0, 0),
            (20, 20),
        )
        maze_generator.generate()
        maze = maze_generator.maze
        graphic = Graphics()
        maze_sprites = SpriteSheetManager("sprites/maze_sprites/maze_sprites.bmp",
                                  "sprites/maze_sprites/maze_sprites.yaml")

        img_width = 900
        img_height = 900

        img = graphic.new_image(img_width, img_height)

        x_dest = (img_width // 2) - (((maze_width // 2) * 8) * 3)
        y_dest = (img_height // 2) - (((maze_height // 2) * 8) * 3)

        print(x_dest)
        print(y_dest, "should be 450")

        for y in range(len(maze)):
            for x in range(len(maze[y])):

                if x == 0 and y == 0:
                    sprite = maze_sprites.get_sprite("wall_double_outer_corner_top_left")
                    graphic.put_sprite_in_image(img, x_dest + x * 8 * 3, y_dest + y * 8 * 3, sprite)
                    continue
                if x == len(maze[0]) - 1 and y == 0:
                    sprite = maze_sprites.get_sprite("wall_double_outer_corner_top_right")
                    graphic.put_sprite_in_image(img, x_dest + x * 8 * 3, y_dest + y * 8 * 3, sprite)
                    continue
                if x == 0 and y == len(maze) - 1:
                    sprite = maze_sprites.get_sprite("wall_double_outer_corner_bottom_left")
                    graphic.put_sprite_in_image(img, x_dest + x * 8 * 3, y_dest + y * 8 * 3, sprite)
                    continue
                if x == len(maze[0]) - 1 and y == len(maze) - 1:
                    sprite = maze_sprites.get_sprite("wall_double_outer_corner_bottom_right")
                    graphic.put_sprite_in_image(img, x_dest + x * 8 * 3, y_dest + y * 8 * 3, sprite)
                    continue

                if x == 0:
                    sprite = maze_sprites.get_sprite("wall_double_vertical_left")
                    graphic.put_sprite_in_image(img, x_dest + x * 8 * 3, y_dest + y * 8 * 3, sprite)
                    continue

                if x == len(maze[0]) - 1:
                    sprite = maze_sprites.get_sprite("wall_double_vertical_right")
                    graphic.put_sprite_in_image(img, x_dest + x * 8 * 3, y_dest + y * 8 * 3, sprite)
                    continue

                if y == 0:
                    sprite = maze_sprites.get_sprite("wall_double_horizontal_top")
                    graphic.put_sprite_in_image(img, x_dest + x * 8 * 3, y_dest + y * 8 * 3, sprite)
                    continue

                if y == len(maze) - 1:
                    sprite = maze_sprites.get_sprite("wall_double_horizontal_bottom")
                    graphic.put_sprite_in_image(img, x_dest + x * 8 * 3, y_dest + y * 8 * 3, sprite)
                    continue

                if maze[y][x] & 1:
                    sprite = maze_sprites.get_sprite("wall_single_horizontal_top")
                    graphic.put_sprite_in_image(img, x_dest + x * 8 * 3, y_dest + y * 8 * 3, sprite)
                if maze[y][x] & 2:
                    sprite = maze_sprites.get_sprite("wall_single_vertical_right")
                    graphic.put_sprite_in_image(img, x_dest + x * 8 * 3, y_dest + y * 8 * 3, sprite)
                if maze[y][x] & 3:
                    sprite = maze_sprites.get_sprite("wall_single_horizontal_bottom")
                    graphic.put_sprite_in_image(img, x_dest + x * 8 * 3, y_dest + y * 8 * 3, sprite)
                if maze[y][x] & 4:
                    sprite = maze_sprites.get_sprite("wall_single_vertical_left")
                    graphic.put_sprite_in_image(img, x_dest + x * 8 * 3, y_dest + y * 8 * 3, sprite)
        return (img)
