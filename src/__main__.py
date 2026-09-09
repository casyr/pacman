import sys
import logging
from .utils import setup_logging
from .parsing import ConfigParser
from .errors import PacmanError

from .view import Graphics


def main() -> int:
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting the application Pacman...")
    graphic = Graphics()

    graphic.initialisation()
    screen = graphic.new_window(800, 800)
    img = graphic.new_image(800, 800)
    # graphic.load_sprite("sprites/pacman_sprite.bmp")
    while (True):
        graphic.put_sprite_in_image(
            img, 100, 100, "sprites/pacman_sprite.bmp",
            0, 0, 16, 16, 225, 3
        )
        graphic.blit_img(img, screen, (100, 100))
        graphic.update_window()

    try:
        loader = ConfigParser(sys.argv[1:])
        game_config = loader.load()
        logger.debug(game_config.pacgum)
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
