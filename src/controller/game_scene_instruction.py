from .game_controller import GameController
from .game_scene import GameScene
from .game_scene_menu import MenuScene


class InstructionScene:
    def update(
            self,
            controller: GameController,
            elapsed_time: float, user_input: str | None) -> GameScene | None:

        if user_input == "KEY_1":
            return MenuScene()
        return self

    def render(self, controller: GameController) -> None:
        # controller.view.draw_instruction_screen(controller)
        # self.view.draw_instruction_screen(controller)
        pass
