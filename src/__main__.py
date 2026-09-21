import sys
import logging
from .utils import setup_logging
from .parsing import ConfigParser
from .errors import PacmanError
from .view import Graphic
from .view import SpriteSheetManager
from .view import MazeRenderer
from mazegenerator import MazeGenerator
import screeninfo


def main() -> int:
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting the application Pacman...")
    try:
        loader = ConfigParser(sys.argv[1:])
        game_config = loader.load()
        logger.debug(game_config.pacgum)
        screen_width = screeninfo.get_monitors()[0].width
        screen_height = screeninfo.get_monitors()[0].height
        graphic = Graphic()
        screen = graphic.new_window(screen_width, screen_height)

        maze_sprite = SpriteSheetManager("sprites/maze_sprites/"
                                         "maze_sprite.bmp",
                                         "sprites/maze_sprites/"
                                         "maze_sprites.yaml")
        Maze_renderer = MazeRenderer(maze_sprite)

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
        img = graphic.new_image(screen_width, screen_height)
        maze_img = Maze_renderer.render_in_img(maze, maze_width,
                                               maze_height, maze_sprite,
                                               img, screen_height, screen_width)
        while (True):
            graphic.blit_img(maze_img, screen, (0, 0))
            graphic.update_window()
        return 0

    except PacmanError as error:
        logger.error(f"Application error [{type(error).__name__}]: {error}")
        return 1

    except KeyboardInterrupt:
        logger.warning("Manual interruption by the user.")
        return 130

    except Exception as e:
        logger.critical(f"Unexpected Crash: {e}", exc_info=True)
        return 2


if __name__ == '__main__':
    sys.exit(main())
