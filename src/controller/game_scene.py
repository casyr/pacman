from typing import Protocol
from .game_scene_commun_object import GameContext


class GameScene(Protocol):
    def update(
            self,
            controller: GameContext,
            elapsed_time: float, user_input: str | None) -> GameScene | None:
        pass

    def render(self, controller: GameContext) -> None:
        pass
