from .game_scene_commun_object import GameContext
from .game_scene import GameScene
from .game_scene_enter_score import ScoreScene


class VictoryScene:
    def update(
            self,
            controller: GameContext,
            elapsed_time: float, user_input: str | None) -> GameScene | None:
        return ScoreScene()

    def render(self, controller: GameContext) -> None:
        # controller.view.draw_victory_screen(
        # controller, controller.game_session.score)
        # self.view.draw_victory_screen(
        # controller, controller.game_session.score)
        pass
