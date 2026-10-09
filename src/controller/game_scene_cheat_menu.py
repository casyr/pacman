from .game_scene_commun_object import GameContext
from ..model import GameStatus
from .game_scene import GameScene


class CheatScene:
    """Scene for toggling cheats during a game."""

    def __init__(self, previous_scene: GameScene):
        """Create a cheat menu linked to the paused scene.

        Args:
            previous_scene: Scene to return to when cheats are closed.
        """
        from .game_scene_victory import VictoryScene
        from .game_scene_playing import PlayingScene
        self.previous_scene = previous_scene
        self.victory_scene = VictoryScene()
        self.playing_scene = PlayingScene()

    def update(
            self,
            controller: GameContext,
            elapsed_time: float,
            user_input: str | None) -> GameScene | None:
        """Apply cheat input and choose the next scene.

        Args:
            controller: Shared game state and service dependencies.
            elapsed_time: Time elapsed since the previous update, in seconds.
            user_input: Input received during this frame, if any.

        Returns:
            The next scene or this scene if no transition occurs.
        """

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
                return self.victory_scene
            controller.game_board = controller.level_manager.build_level()
            controller.view.playing_view.clear_all_layers()
            controller.game_session.time_remaining = float(
                controller.game_session.settings.level_max_time)
            controller.view.load_maze(controller.game_board)
            return self.playing_scene
        elif user_input == "KEY_6":
            controller.game_session.cheat_add_score()
        elif user_input == "KEY_C":
            controller.game_session.switch_status_paused()
            return self.previous_scene
        return self

    def render(self, controller: GameContext) -> None:
        """Draw the cheat menu.

        Args:
            controller: Shared game state and service dependencies.
        """
        controller.view.draw_cheat()
