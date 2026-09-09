import sys
import logging
from .utils import setup_logging
from .parsing import ConfigParser
from .errors import PacmanError

from .view import Graphics
from .view import SpriteSheet


def main() -> int:
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting the application Pacman...")
    try:
        loader = ConfigParser(sys.argv[1:])
        game_config = loader.load()
        logger.debug(game_config.pacgum)
        graphic = Graphics()
        pacman = SpriteSheet("sprites/pacman_sprite.bmp")
        pacman.get_sprite_data()
        graphic.initialisation()
        screen = graphic.new_window(800, 800)
        img = graphic.new_image(800, 800)
        while (True):
            graphic.put_sprite_in_image(
                img, 100, 100, pacman.sprite_fill_data("pacman_right_1"))
            graphic.blit_img(img, screen, (100, 100))
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
