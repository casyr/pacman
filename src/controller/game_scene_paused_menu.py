from .game_context import GameContext
from .game_scene import GameScene


class PausedScene:
    def __init__(self, previous_scene: GameScene):
        self.previous_scene = previous_scene

    def update(
            self,
            controller: GameContext,
            elapsed_time: float, user_input: str | None) -> GameScene | None:
        from .game_scene_menu import MenuScene

        if user_input == "KEY_1":
            controller.game_session.switch_status_paused()
            return self.previous_scene
        elif user_input == "KEY_2":
            controller.game_session.switch_status_paused()
            return MenuScene()
        return self

    def render(self, controller: GameContext) -> None:
        # controller.view.draw_pause_menu()
        # self.draw_pause_menu()
        pass
