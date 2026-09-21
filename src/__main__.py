import sys
import logging
from .utils import setup_logging
from .errors import PacmanError
from .controller import GameController


def main() -> int:
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting the application Pacman...")
    if len(sys.argv) != 2:
        logger.error("Use: uv run python3 -m src src/config.json")
        return 1
    config_file_path: str = sys.argv[1]

    try:
        controller = GameController(config_file_path)
        logger.info(controller.highscore_manager)
        logger.info(controller.game_board.ghosts_spawn_pos)
        controller.run()
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
