from . import SpriteSheetManager
from mazegenerator import MazeGenerator
from .graphics import Graphics


class MazeRenderer:

    def render_in_img(self) -> pygame.Surface:
        maze_generator = MazeGenerator(
            (21, 21),
            False,
            (0, 0),
            (20, 20),
        )
        maze_generator.generate()
        maze = maze_generator.maze
        graphic = Graphics()
        maze_sprites = SpriteSheetManager("sprites/maze_sprites/maze_sprite.bmp",
                                  "sprites/maze_sprites/maze_sprites.yaml")
        img = graphic.new_image(1800, 1800)
        for y in range(len(maze)):
            for x in range(len(maze[y])):
                if maze[y][x] & 1:
                    sprite = maze_sprites.get_sprite("wall_double_horizontal_top")
                    graphic.put_sprite_in_image(img, x * 8 * 3, y * 8 * 3, sprite)
                if maze[y][x] & 2:
                    sprite = maze_sprites.get_sprite("wall_double_vertical_right")
                    graphic.put_sprite_in_image(img, x * 8 * 3, y * 8 * 3, sprite)
                if maze[y][x] & 3:
                    sprite = maze_sprites.get_sprite("wall_double_horizontal_bottom")
                    graphic.put_sprite_in_image(img, x * 8 * 3, y * 8 * 3, sprite)
                if maze[y][x] & 4:
                    sprite = maze_sprites.get_sprite("wall_double_vertical_left")
                    graphic.put_sprite_in_image(img, x * 8 * 3, y * 8 * 3, sprite)
        return (img)
