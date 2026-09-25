from .game_controller import GameController
from .game_scene import GameScene
from .game_scene_enter_score import ScoreScene


class VictoryScene:
    def update(
            self,
            controller: GameController,
            elapsed_time: float, user_input: str | None) -> GameScene | None:
        return ScoreScene()

    def render(self, controller: GameController) -> None:
        # controller.view.draw_victory_screen(
        # controller, controller.game_session.score)
        # self.view.draw_victory_screen(
        # controller, controller.game_session.score)
        pass
