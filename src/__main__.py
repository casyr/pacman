import sys
import logging
from .utils import setup_logging
from .parsing import ConfigParser
from .errors import PacmanError

from .view import Graphics
from .view import SpriteSheetManager
from .view import MazeRenderer


def main() -> int:
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting the application Pacman...")
    try:
        loader = ConfigParser(sys.argv[1:])
        game_config = loader.load()
        logger.debug(game_config.pacgum)
        graphic = Graphics()
        graphic.initialisation()
        screen = graphic.new_window(1800, 1800)
        Maze_renderer = MazeRenderer()
        maze_img = Maze_renderer.render_in_img()
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
