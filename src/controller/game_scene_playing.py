from .game_controller import GameController
from .game_scene import GameScene
from .game_scene_victory import VictoryScene
from .game_scene_defeat import DefeatScene
from .game_scene_paused_menu import PausedScene
from .game_scene_cheat_menu import CheatScene
from ..shared import GhostState, Vector2D
from ..model import GameStatus


class PlayingScene:
    def update(
            self,
            controller: GameController,
            elapsed_time: float, user_input: str | None) -> GameScene | None:

        scene = self._check_game_end_conditions(controller)
        if scene is not PlayingScene:
            return scene

        scene = self._handle_playing_inputs(user_input, controller)
        if scene is not PlayingScene:
            return scene

        self._update_player_and_timers(elapsed_time, controller)

        player_pos = Vector2D(
            y=controller.game_board.player.current_pos_y,
            x=controller.game_board.player.current_pos_x
        )

        self._handle_consumables(controller, player_pos)
        self._handle_ghosts_and_collisions(
            controller, player_pos, elapsed_time)

        return self

    def _check_game_end_conditions(
            self,
            controller: GameController
            ) -> GameScene:

        if controller.game_session.game_status == GameStatus.GAME_OVER:
            return DefeatScene()
        elif controller.game_session.game_status == GameStatus.VICTORY:
            return VictoryScene()
        return self

    def _handle_playing_inputs(
            self,
            user_input: str | None,
            controller: GameController
            ) -> GameScene:

        if user_input == "KEY_P":
            controller.game_session.switch_status_paused()
            return PausedScene(previous_scene=self)

        elif user_input == "KEY_C":
            controller.game_session.switch_status_paused()
            return CheatScene(previous_scene=self)

        elif user_input == "KEY_T":
            return VictoryScene()

        if user_input == "KEY_W":
            controller.game_board.player.set_direction(-1, 0)
        elif user_input == "KEY_S":
            controller.game_board.player.set_direction(1, 0)
        elif user_input == "KEY_A":
            controller.game_board.player.set_direction(0, -1)
        elif user_input == "KEY_D":
            controller.game_board.player.set_direction(0, 1)

        return self

    def _update_player_and_timers(
            self,
            elapsed_time: float,
            controller: GameController) -> None:

        controller.game_session.update_timers(elapsed_time)
        controller.game_board.player.update(
            elapsed_time * controller.game_session.speed_multiplier)

    def _handle_consumables(
            self,
            controller: GameController,
            player_pos: Vector2D) -> None:

        if player_pos in controller.game_board.pacgum_pos:
            controller.game_board.pacgum_pos.remove(player_pos)
            controller.game_session.consume_pacgum()

        if player_pos in controller.game_board.super_pacgums_pos:
            controller.game_board.super_pacgums_pos.remove(player_pos)
            controller.game_session.consume_super_pacgum()

            for ghost in controller.game_board.ghosts:
                if ghost.state != GhostState.EATEN:
                    ghost.state = GhostState.FRIGHTENED

    def _handle_ghosts_and_collisions(
            self,
            controller: GameController,
            player_pos: Vector2D,
            elapsed_time: float) -> None:

        if controller.game_session.cheat_mode.freeze:
            return

        for ghost in controller.game_board.ghosts:
            ghost.update(elapsed_time)
            ghost_pos = Vector2D(y=ghost.current_pos_y, x=ghost.current_pos_x)

            if controller.game_session.power_just_expired:
                ghost.state = GhostState.NORMAL

            if player_pos == ghost_pos:
                if (controller.game_session.active_power and
                        ghost.state == GhostState.FRIGHTENED):

                    ghost.get_eaten()
                    controller.game_session.consume_ghost()

                elif ghost.state == GhostState.NORMAL:
                    if controller.game_session.lose_life():
                        controller.game_board.reset_entities()
                        return

    def render(self, controller: GameController) -> None:
        # controller.view.draw_game(
        # controller.game_board, controller.game_session)
        # self.view.draw_game(controller.game_board, controller.game_session)
        pass
