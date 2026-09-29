import time
import logging
from .game_context import GameContext
from .game_scene import GameScene
from .game_scene_menu import MenuScene
from ..model import (
    GameSession,
    LevelBuilder,
    HighScoreManager,
)
from pygame import Surface
from ..view.sprite_sheet_manager import SpriteSheetsManager
from ..view import mlx_wrapper as mlx
import pygame
# from ..view import GameView


logger = logging.getLogger(__name__)


class GameController:
    def __init__(
            self, context: GameContext):

        self.context = context

        self.current_scene: GameScene | None = MenuScene()

        self.last_time = time.perf_counter()
        self.target_fps: int = 60
        self.frame_duration: float = 1.0 / self.target_fps


    def handle_events(self) -> str | None:
        key: str | None = None
        for event in mlx.get_events():
            print("Pygame event:", event)
            if event.type == pygame.QUIT:
                return "MOUSE_QUIT"
            action = mlx.get_key_pressed(event)
            if action is not None:
                key = action
        return key

    def run(self, context: GameContext) -> None:
        while self.current_scene is not None:
            current_time = time.perf_counter()
            elapsed_time = current_time - self.last_time
            self.last_time = current_time

            user_input = self.handle_events()
            self.current_scene = self.current_scene.update(
                self.context, elapsed_time, user_input)
            if self.current_scene is not None:
                self.current_scene.render(self.context)

            processing_time = time.perf_counter() - self.last_time
            time_to_sleep = self.frame_duration - processing_time
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)
