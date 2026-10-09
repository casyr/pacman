from .game_scene_commun_object import GameContext
from .game_scene import GameScene
from .game_scene_menu import MenuScene


class InstructionScene:
    """Scene that displays the game instructions."""

    def update(
            self,
            controller: GameContext,
            elapsed_time: float, user_input: str | None) -> GameScene | None:
        """Return to the main menu when requested.

        Args:
            controller: Shared game state and service dependencies.
            elapsed_time: Time elapsed since the previous update, in seconds.
            user_input: Input received during this frame, if any.

        Returns:
            The menu scene or this scene if no transition occurs.
        """

        if user_input == "KEY_1":
            return MenuScene()
        return self

    def render(self, controller: GameContext) -> None:
        """Draw the instruction screen.

        Args:
            controller: Shared game state and service dependencies.
        """
        controller.view.clear_window()
        controller.view.draw_instruction()
