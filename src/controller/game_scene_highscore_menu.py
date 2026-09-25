from .game_controller import GameController
from .game_scene import GameScene


class HighscoreMenuScene:
    def update(
            self,
            controller: GameController,
            elapsed_time: float, user_input: str | None) -> GameScene | None:
        pass

    def render(self, controller: GameController) -> None:
        # controller.view.draw_highscore_screen(
        # controller, controller.highscore_manager.scores)
        # self.view.draw_highscore_screen(
        # controller, controller.highscore_manager.scores)
        pass
