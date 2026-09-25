from typing import Protocol
from .game_controller import GameController


class GameScene(Protocol):
    def update(
            self,
            controller: GameController,
            elapsed_time: float, user_input: str | None) -> GameScene | None:
        pass

    def render(self, controller: GameController) -> None:
        pass
