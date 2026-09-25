import time
import logging
from .game_scene import GameScene
from .game_scene_menu import MenuScene
from ..model import (
    GameSession,
    LevelBuilder,
    HighScoreManager,
)
from ..view import GameView


logger = logging.getLogger(__name__)


class GameController:
    def __init__(
            self,
            level_manager: LevelBuilder,
            highscore_manager: HighScoreManager,
            game_session: GameSession,
            game_view: GameView):

        self.level_manager = level_manager
        self.highscore_manager = highscore_manager
        self.game_session = game_session
        self.view = game_view

        self.game_board = self.level_manager.build_level()

        self.current_scene: GameScene | None = MenuScene()

        self.last_time = time.perf_counter()
        self.target_fps: int = 60
        self.frame_duration: float = 1.0 / self.target_fps

    def run(self) -> None:
        self.view.initialize_graphics()
        # self.view.load_assets()
        while self.current_scene is not None:
            current_time = time.perf_counter()
            elapsed_time = current_time - self.last_time
            self.last_time = current_time

            user_input = self.view.handle_events()

            self.current_scene = self.current_scene.update(
                self, elapsed_time, user_input)
            if self.current_scene is not None:
                self.current_scene.render(self)

            processing_time = time.perf_counter() - self.last_time
            time_to_sleep = self.frame_duration - processing_time
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)
        self.view.close()
