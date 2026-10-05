from .game_scene_commun_object import GameContext
from .game_scene import GameScene
from .game_scene_menu import MenuScene
from .game_scene_playing import PlayingScene


class HighscoreMenuScene:
    def update(
            self,
            controller: GameContext,
            elapsed_time: float, user_input: str | None) -> GameScene | None:

        if user_input == "KEY_1":
            return MenuScene()
        if user_input == "KEY_SPACE":
            controller.game_session.reset_level_data()
            controller.game_board = controller.level_manager.build_level()
            controller.view.load_maze(controller.game_board)
            return PlayingScene()
        return self

    def render(self, controller: GameContext) -> None:
        controller.view.clear_window()
        controller.view.draw_highscores(
            controller.highscores.load_score())
