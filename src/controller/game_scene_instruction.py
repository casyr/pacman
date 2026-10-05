from .game_scene_commun_object import GameContext
from .game_scene import GameScene
from .game_scene_menu import MenuScene


class InstructionScene:
    def update(
            self,
            controller: GameContext,
            elapsed_time: float, user_input: str | None) -> GameScene | None:

        if user_input == "KEY_1":
            return MenuScene()
        return self

    def render(self, controller: GameContext) -> None:
        controller.view.clear_window()
        controller.view.draw_instruction()
