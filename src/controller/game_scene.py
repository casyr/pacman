from __future__ import annotations
from typing import Protocol
from .game_context import GameContext


class GameScene(Protocol):

    def __init__(self, context: GameContext):
        self.context = context

    def update(self, controller: GameContext, lapsed_time: float,
               user_input: str | None) -> GameScene | None:
        pass

    def render(self) -> None:
        pass
