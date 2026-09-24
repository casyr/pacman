import sys
import logging
from .model import HighScoreManager, GameSession, LevelBuilder
from .utils import setup_logging, JsonModelLoader
from .parsing import ConfigParser
from .errors import PacmanError
import time
from .view import Pacgums, SpriteSheetManager, GameView, Maze


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
        # highscore_manager = HighScoreManager(json_loader)
        game_session: GameSession = GameSession(game_config)
        level_manager = LevelBuilder(game_session)
        game_board = level_manager.build_level()
        view = GameView(game_session.settings.levels[0].width,
                        game_session.settings.levels[0].height)
        view.graphic.initialisation()
        screen = view.graphic.new_window(view.screen_width, view.screen_width)
        img = view.graphic.new_image(view.screen_width, view.screen_width)
        maze_sprite = SpriteSheetManager("sprites/maze_sprites/maze_sprites.bmp",
                                    "sprites/maze_sprites/maze_sprites.yaml",
                                    img)
        pacgum = Pacgums(game_session.settings.levels[0].width,
                         game_session.settings.levels[0].height,
                         game_board.pacgum_pos,
                         maze_sprite.get_sprite("pacgum_small"))

        maze = Maze(game_session.settings.levels[0].width,
                         game_session.settings.levels[0].height,
                         maze_sprite,
                         game_board.maze.grid)

        maze.render(view.graphic.to_buffer(img),
                      view.screen_width)

        pacgum.render(view.graphic.to_buffer(img),
                      view.screen_width)
        while (True):
            view.blit_and_update(img, screen)
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
