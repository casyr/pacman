from .game_scene_commun_object import GameContext
from .game_scene import GameScene
from .game_scene_menu import MenuScene
from .game_scene_playing import PlayingScene


class HighscoreMenuScene:
    """Scene for viewing high scores or starting a new game."""

    def update(
            self,
            controller: GameContext,
            elapsed_time: float, user_input: str | None) -> GameScene | None:
        """Handle high-score menu input.

        Args:
            controller: Shared game state and service dependencies.
            elapsed_time: Time elapsed since the previous update, in seconds.
            user_input: Input received during this frame, if any.

        Returns:
            The selected scene or this scene if no transition occurs.
        """

        if user_input == "KEY_1":
            return MenuScene()
        if user_input == "KEY_SPACE":
            controller.game_session.reset_level_data()
            controller.game_board = controller.level_manager.build_level()
            controller.view.load_maze(controller.game_board)
            return PlayingScene()
        return self

    def render(self, controller: GameContext) -> None:
        """Draw the high-score list.

        Args:
            controller: Shared game state and service dependencies.
        """
        controller.view.clear_window()
        controller.highscores.load_score()
        controller.view.draw_highscores(controller.highscores.scores)
