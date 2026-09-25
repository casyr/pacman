from .game_controller import GameController
from .game_scene import GameScene
from .game_scene_menu import MenuScene


class PausedScene:
    def __init__(self, previous_scene: GameScene):
        self.previous_scene = previous_scene

    def update(
            self,
            controller: GameController,
            elapsed_time: float, user_input: str | None) -> GameScene | None:

        if user_input == "KEY_1":
            controller.game_session.switch_status_paused()
            return self.previous_scene
        elif user_input == "KEY_2":
            controller.game_session.switch_status_paused()
            return MenuScene()
        return self

    def render(self, controller: GameController) -> None:
        # controller.view.draw_pause_menu()
        # self.draw_pause_menu()
        pass
