import sys
import logging
from utils.config_logging import setup_logging
from parsing.parser import ConfigParser
from utils.file_loader_json import JsonModelLoader
from model.high_score_manager import HighScoreManager
from exceptions import (
    PacmanError,
    ParserError,
    GameSettingsError,
    ModelError,
    JsonLoadError,
    ViewError,
    ControllerError
)


def main() -> int:
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting the application Pacman...")

    try:
        loader = ConfigParser(sys.argv[1:])
        game_config = loader.load()
        score_json_loader = JsonModelLoader(game_config.highscore_filename)
        score_manager = HighScoreManager(score_json_loader)
        data = score_manager.load_score()
        logger.debug(game_config)
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
        logger.error(f"Raised during operation on json file: {e}")
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
