from .game_context import GameContext
from .game_scene import GameScene
from ..view import mlx_wrapper as mlx


class MenuScene:
    def update(
            self,
            context: GameContext,
            elapsed_time: float, user_input: str | None) -> GameScene | None:
        from .game_scene_playing import PlayingScene
        from .game_scene_highscore_menu import HighscoreMenuScene
        from .game_scene_instruction import InstructionScene

        if user_input == "KEY_1":
            context.game_session.reset_level_data()
            context.game_board = context.level_manager.build_level()
            return PlayingScene(context)
        elif user_input == "KEY_2":
            return HighscoreMenuScene()
        elif user_input == "KEY_3":
            return InstructionScene()
        elif user_input in ("KEY_4", "KEY_ESCAPE", "MOUSE_QUIT"):
            return None
        return self

    def render(self, context: GameContext) -> None:
        mlx.clear_window(context.window)
        # controller.view.draw_main_menu()
        # self.view.draw_main_menu()
        pass
