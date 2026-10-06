from .game_scene_commun_object import GameContext
from ..model import GameStatus
from .game_scene import GameScene


class CheatScene:
    def __init__(self, previous_scene: GameScene):
        self.previous_scene = previous_scene

    def update(
            self,
            controller: GameContext,
            elapsed_time: float,
            user_input: str | None) -> GameScene | None:
        from .game_scene_victory import VictoryScene
        from .game_scene_playing import PlayingScene

        if user_input == "KEY_1":
            controller.game_session.switch_invincibility()
        elif user_input == "KEY_2":
            controller.game_session.switch_ghost_freeze()
        elif user_input == "KEY_3":
            controller.game_session.switch_speed_boost()
        elif user_input == "KEY_4":
            controller.game_session.cheat_extra_lives()
        elif user_input == "KEY_5":
            controller.game_session.cheat_skip_level()
            if controller.game_session.game_status == GameStatus.VICTORY:
                return VictoryScene()
            controller.game_board = controller.level_manager.build_level()
            controller.game_session.next_level_data()
            return PlayingScene()
        elif user_input == "KEY_6":
            controller.game_session.cheat_add_score()
        elif user_input == "KEY_C":
            controller.game_session.switch_status_paused()
            return self.previous_scene
        return self

    def render(self, controller: GameContext) -> None:
        controller.view.draw_cheat()
