from .game_scene_commun_object import GameContext
from .game_scene import GameScene


class PausedScene:
    """Pause menu that resumes play or returns to the main menu."""

    def __init__(self, previous_scene: GameScene):
        """Create a pause menu linked to the scene being paused.

        Args:
            previous_scene: Scene to resume when play is selected.
        """
        self.previous_scene = previous_scene

    def update(
            self,
            controller: GameContext,
            elapsed_time: float, user_input: str | None) -> GameScene | None:
        """Handle pause menu input and select the next scene.

        Args:
            controller: Shared game state and service dependencies.
            elapsed_time: Time elapsed since the previous update, in seconds.
            user_input: Input received during this frame, if any.

        Returns:
            The selected scene or this scene if no transition occurs.
        """
        from .game_scene_menu import MenuScene

        if user_input == "KEY_1":
            controller.game_session.switch_status_paused()
            return self.previous_scene
        elif user_input == "KEY_2":
            controller.game_session.switch_status_paused()
            return MenuScene()
        return self

    def render(self, controller: GameContext) -> None:
        """Draw the pause menu.

        Args:
            controller: Shared game state and service dependencies.
        """
        controller.view.draw_paused()
