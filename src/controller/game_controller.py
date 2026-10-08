import time
import logging
from .game_scene_commun_object import GameContext
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

        self.context = GameContext(
            game_session,
            level_manager,
            highscore_manager,
            game_view
        )
        self.frame_count = 0
        self.fps_timer = 0.0
        self.current_fps = 0.0

        self.current_scene: GameScene | None = MenuScene()

        self.last_time = time.perf_counter()
        self.target_fps: int = 60
        self.frame_duration: float = 1.0 / self.target_fps

    def run(self) -> None:

        while self.current_scene is not None:

            current_time = time.perf_counter()
            elapsed_time = current_time - self.last_time
            self.last_time = current_time
            self.frame_count += 1
            self.fps_timer += elapsed_time
            if self.fps_timer >= 1.0:
                self.current_fps = self.frame_count / self.fps_timer
                self.frame_count = 0
                self.fps_timer = 0.0
                logger.debug(f"current FPS : {self.current_fps:.1f}")
            user_input = self.context.view.handle_events()
            self.current_scene = self.current_scene.update(
                self.context, elapsed_time, user_input)
            if self.current_scene is not None:
                self.current_scene.render(self.context)

            processing_time = time.perf_counter() - self.last_time
            time_to_sleep = self.frame_duration - processing_time
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)
