from .game_controller import GameController
from .game_scene import GameScene
from .game_scene_playing import PlayingScene
from .game_scene_highscore_menu import HighscoreMenuScene
from .game_scene_instruction import InstructionScene


class MenuScene:
    def update(
            self,
            controller: GameController,
            elapsed_time: float, user_input: str | None) -> GameScene | None:

        if user_input == "KEY_1":
            controller.game_session.reset_level_data()
            controller.game_board = controller.level_manager.build_level()
            return PlayingScene()
        elif user_input == "KEY_2":
            return HighscoreMenuScene()
        elif user_input == "KEY_3":
            return InstructionScene()
        elif user_input == "KEY_4":
            return None

        return self

    def render(self, controller: GameController) -> None:
        # controller.view.draw_main_menu()
        # self.view.draw_main_menu()
        pass
