from .game_scene_commun_object import GameContext
from .game_scene import GameScene
from .game_scene_menu import MenuScene
from ..model import HighScore


class ScoreScene:
    def update(
            self,
            controller: GameContext,
            elapsed_time: float, user_input: str | None) -> GameScene | None:

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
        elif user_input.startswith("KEY_"):
            controller.game_session.player_name += user_input[4:].lower()
        elif user_input.startswith("CHAR_"):
            controller.game_session.player_name += user_input[5:]

        return self

    def render(self, controller: GameContext) -> None:
        controller.view.clear_window()
        # controller.view.draw_enter_name_screen(controller)
        # self.view.draw_enter_name_screen(controller)
        pass
