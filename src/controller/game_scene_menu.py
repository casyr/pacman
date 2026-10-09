from .game_scene_commun_object import GameContext
from .game_scene import GameScene


class MenuScene:
    """Main menu scene for starting and navigating the game."""

    def __init__(self) -> None:
        """Initialize the menu and its destination scenes."""
        from .game_scene_playing import PlayingScene
        from .game_scene_highscore_menu import HighscoreMenuScene
        from .game_scene_instruction import InstructionScene

        self.playing_scene = PlayingScene()
        self.highscore_scene = HighscoreMenuScene()
        self.instruction_scene = InstructionScene()

    def update(
            self,
            controller: GameContext,
            elapsed_time: float, user_input: str | None) -> GameScene | None:
        """Handle menu input and choose the next scene.

        Args:
            controller: Shared game state and service dependencies.
            elapsed_time: Time elapsed since the previous update, in seconds.
            user_input: Input received during this frame, if any.

        Returns:
            The selected scene, this scene, or None to exit.
        """

        if user_input == "KEY_1" or user_input == "KEY_SPACE":
            controller.game_session.reset_level_data()
            controller.game_board = controller.level_manager.build_level()
            controller.view.load_maze(controller.game_board)
            return self.playing_scene
        elif user_input == "KEY_2":
            return self.highscore_scene
        elif user_input == "KEY_3":
            return self.instruction_scene
        elif user_input in ("KEY_4", "KEY_ESCAPE", "MOUSE_QUIT"):
            return None
        return self

    def render(self, controller: GameContext) -> None:
        """Draw the main menu.

        Args:
            controller: Shared game state and service dependencies.
        """
        controller.view.clear_window()
        controller.view.draw_menu()
