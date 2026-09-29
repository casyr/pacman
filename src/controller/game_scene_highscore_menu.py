from .game_context import GameContext
from .game_scene import GameScene


class HighscoreMenuScene:
    def update(
            self,
            controller: GameContext,
            elapsed_time: float, user_input: str | None) -> GameScene | None:
        pass

    def render(self, controller: GameContext) -> None:
        controller.view.clear_window()
        # controller.view.draw_highscore_screen(
        # controller, controller.highscore_manager.scores)
        # self.view.draw_highscore_screen(
        # controller, controller.highscore_manager.scores)
        pass
