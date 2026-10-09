from .game_scene_commun_object import GameContext
from .game_scene import GameScene
from .game_scene_menu import MenuScene
from ..model import HighScore
from ..model import GameStatus


class ScoreScene:
    """Scene for entering and saving the player's high-score name."""

    def update(
            self,
            controller: GameContext,
            elapsed_time: float, user_input: str | None) -> GameScene | None:
        """Process name-entry input and save valid scores.

        Args:
            controller: Shared game state and service dependencies.
            elapsed_time: Time elapsed since the previous update, in seconds.
            user_input: Input received during this frame, if any.

        Returns:
            The menu scene after saving, or this scene otherwise.
        """

        if user_input is None:
            return self

        if user_input == "KEY_RETURN":
            if not HighScore._handle_player_names(
                    controller.game_session.player_name.strip()):
                controller.game_session.player_name = ""
            else:
                controller.highscores.update_score(
                    controller.game_session.player_name,
                    controller.game_session.score)
                controller.game_session.reset_level_data()
                return MenuScene()
        elif user_input == "KEY_BACKSPACE":
            controller.game_session.player_name = (
                controller.game_session.player_name[:-1])
        elif user_input == "KEY_SPACE":
            if len(controller.game_session.player_name) < 10:
                controller.game_session.player_name += " "
        elif user_input.startswith("KEY_"):
            if len(controller.game_session.player_name) < 10:
                controller.game_session.player_name += user_input[4:].lower()
        elif user_input.startswith("CHAR_"):
            if len(controller.game_session.player_name) < 10:
                controller.game_session.player_name += user_input[5:]
        return self

    def render(self, controller: GameContext) -> None:
        """Draw the score-entry screen for the game outcome.

        Args:
            controller: Shared game state and service dependencies.
        """
        controller.view.clear_window()
        if (controller.game_session.game_status == GameStatus.VICTORY):
            controller.view.victory.render_enter_score(
                controller.game_session.score,
                controller.game_session.player_name
            )
        else:
            controller.view.defeat.render_enter_score(
                controller.game_session.score,
                controller.game_session.player_name
            )
