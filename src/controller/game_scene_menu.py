from .game_scene_commun_object import GameContext
from .game_scene import GameScene


class MenuScene:

    def __init__(self) -> None:
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
        controller.view.clear_window()
        controller.view.draw_menu()
