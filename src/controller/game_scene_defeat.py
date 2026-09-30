from .game_context import GameContext
from .game_scene_enter_score import ScoreScene


class DefeatScene:
    def update(
            self,
            controller: GameContext,
            elapsed_time: float, user_input: str | None) -> ScoreScene:
        return ScoreScene()

    def render(self, controller: GameContext) -> None:
        # controller.clear_window()
        # controller.view.draw_defeat_screen(
        # controller, controller.game_session.score)
        # self.view.draw_defeat_screen(
        # controller, controller.game_session.score)
        pass
