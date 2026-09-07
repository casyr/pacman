import sys
import logging
from src.utils.config_logging import setup_logging
from src.parsing.parser import ConfigParser
from src.exceptions import (
    PacmanError,
    ParserError,
    GameSettingsError,
    ModelError,
    JsonLoadError,
    ViewError,
    ControllerError
)
from src.view.graphics import Graphics


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
        screen = graphic.new_window(800, 800)
        image = graphic.new_image(800, 800)
        new_image = graphic.put_sprite_in_image(image, 50, 50, "sprites/text_sprite.png", 5, 5, 50, 50)
        while(True):
            graphic.blit_img(new_image, screen, (0, 0))
            graphic.update_window()

        # graphic.quit_window()
        return 0

    except ParserError as e:
        logger.error(f"CLI failed: {e}")
        return 1

    except GameSettingsError as e:
        logger.error(f"Parsing failed: {e}")
        return 1

    except ModelError as e:
        logger.error(f"Raised during a logic rule forbidden: {e}")
        return 1

    except JsonLoadError as e:
        logger.error(f"Raised during a saving json file: {e}")
        return 1

    except ViewError as e:
        logger.error(f"Graphics subsystem error: {e}")
        return 1

    except ControllerError as e:
        logger.error(f"Controller subsystem error: {e}")
        return 1

    except PacmanError as e:
        logger.error(f"Application Pacman error: {e}")
        return 1

    except KeyboardInterrupt:
        logger.warning("Manual interruption by the user.")
        return 130

    except Exception as e:
        logger.critical(f"Unexpected Crash: {e}", exc_info=True)
        return 2


if __name__ == '__main__':
    sys.exit(main())
