import sys
import logging
from .model import HighScoreManager, GameSession, LevelBuilder
from .utils import setup_logging, JsonModelLoader
from .parsing import ConfigParser
from .errors import PacmanError
from mazegenerator import MazeGenerator
import time


def main() -> int:
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting the application Pacman...")
    try:
        config_file_path = "src/config.json"
        loader = ConfigParser(config_file_path)
        game_config = loader.load()
        logger.debug(game_config.pacgum)
        json_loader = JsonModelLoader(game_config.highscore_filename)
        highscore_manager = HighScoreManager(json_loader)
        game_session: GameSession = GameSession(game_config)
        level_manager = LevelBuilder(game_session)
        
        while (True):
            time.sleep(200)
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
