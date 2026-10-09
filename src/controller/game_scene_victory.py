from .game_scene_commun_object import GameContext
from .game_scene import GameScene
from .game_scene_enter_score import ScoreScene


class VictoryScene:
    """Scene shown after the player completes the game."""

    def update(
            self,
            controller: GameContext,
            elapsed_time: float, user_input: str | None) -> GameScene | None:
        """Move to the score-entry scene.

        Args:
            controller: Shared game state and service dependencies.
            elapsed_time: Time elapsed since the previous update, in seconds.
            user_input: Input received during this frame, if any.

        Returns:
            The score-entry scene.
        """
        return ScoreScene()

    def render(self, controller: GameContext) -> None:
        """Draw the victory screen and final score.

        Args:
            controller: Shared game state and service dependencies.
        """
        controller.view.clear_window()
        controller.view.draw_victory(controller.game_session.score)
