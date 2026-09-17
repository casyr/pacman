import sys
import logging

from .model import HighScoreManager, GameSession, LevelBuilder
from .utils import setup_logging, JsonModelLoader
from .parsing import ConfigParser
from .errors import PacmanError


def main() -> int:
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting the application Pacman...")
    if len(sys.argv) != 2:
        logger.error("Use: uv run python3 -m src src/config.json")
        return 1
    config_file_path: str = sys.argv[1]

    try:
        loader = ConfigParser(config_file_path)
        game_config = loader.load()
        json_loader = JsonModelLoader(game_config.highscore_filename)
        file_score_manager = HighScoreManager(json_loader)
        game_session_manager = GameSession(game_config)
        level_manager = LevelBuilder(game_session_manager)
        level_manager.build_level()
        logger.info(file_score_manager)
        logger.info(level_manager.pacgum_pos)
        logger.info(level_manager.pacgum)
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
