from __future__ import annotations
from typing import Protocol
from .game_scene_commun_object import GameContext


class GameScene(Protocol):
    """Protocol for scenes that update and render the game."""

    def update(
            self,
            controller: GameContext,
            elapsed_time: float, user_input: str | None) -> GameScene | None:
        """Update the scene and optionally transition to another scene.

        Args:
            controller: Shared game state and service dependencies.
            elapsed_time: Time elapsed since the previous update, in seconds.
            user_input: Input received during this frame, if any.

        Returns:
            The next scene, or None to stop the game.
        """
        pass

    def render(self, controller: GameContext) -> None:
        """Render this scene.

        Args:
            controller: Shared game state and service dependencies.
        """
        pass
