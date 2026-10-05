import sys
import logging
from screeninfo import get_monitors, ScreenInfoError
from .view import mlx_wrapper as mlx
from .view import SpriteSheetsManager
from .utils import setup_logging
from .errors import PacmanError
from .parsing import ConfigParser
from .model import HighScoreManager, GameSession, LevelBuilder
from .utils import JsonModelLoader
from .controller import GameController
from .view import GameView


def initialize_graphics() -> tuple[int, int]:
    mlx.initialisation()
    monitors = get_monitors()
    if not monitors:
        raise ScreenInfoError("No screen detected")
    return monitors[0].width, monitors[0].height


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
        highscore_manager = HighScoreManager(json_loader)
        game_session: GameSession = GameSession(game_config)
        level_manager = LevelBuilder(game_session)
        screen_width, screen_height = initialize_graphics()
        window = mlx.new_window(screen_width, screen_height)
        sprite = SpriteSheetsManager("sprites")
        sprite.processed_sprite()
        game_view = GameView(screen_width, screen_height, sprite, window)
        controller = GameController(
            level_manager,
            highscore_manager,
            game_session,
            game_view)
        logger.debug(game_session.pacgum_remaining)
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
