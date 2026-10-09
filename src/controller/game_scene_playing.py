from .game_scene_commun_object import GameContext
from .game_scene import GameScene
from .game_scene_paused_menu import PausedScene
from .game_scene_cheat_menu import CheatScene
from ..shared import GhostState, Vector2D, Direction
from ..model import GameStatus


class PlayingScene:
    """Scene that advances gameplay, collisions, and level progression."""

    def __init__(self) -> None:
        """Initialize gameplay and its outcome scenes."""
        from .game_scene_victory import VictoryScene
        from .game_scene_defeat import DefeatScene
        self.victory_scene = VictoryScene()
        self.defeat_scene = DefeatScene()
        self.current_level_index: int | None = None

    def update(
            self,
            controller: GameContext,
            elapsed_time: float, user_input: str | None) -> GameScene | None:
        """Advance gameplay and handle state transitions.

        Args:
            controller: Shared game state and service dependencies.
            elapsed_time: Time elapsed since the previous update, in seconds.
            user_input: Input received during this frame, if any.

        Returns:
            The active scene, an outcome scene, or None to exit.
        """

        scene = self._check_game_end_conditions(controller)
        if scene is not self:
            return scene

        scene = self._handle_playing_inputs(user_input, controller)
        if scene is not self:
            return scene

        self._update_player_and_timers(elapsed_time, controller)
        player = controller.game_board.player
        if player.is_dying:
            if not player.death_animation_finished():
                return self
            controller.game_session.lose_life()
            if controller.game_session.game_status == GameStatus.GAME_OVER:
                return self.defeat_scene
            controller.game_session.update_level_data()
            controller.game_board.reset_entities()
            return self

        player_pixel_pos = self._get_player_pixel_position(controller)
        controller.game_session.check_level_cleared()
        self._handle_ghosts_and_collisions(
            controller, player_pixel_pos, elapsed_time)

        self._handle_consumables(controller, player_pixel_pos)
        self._check_update_level(controller)
        return self

    def _check_game_end_conditions(
            self,
            controller: GameContext
            ) -> GameScene:
        """Select an outcome scene when the session has ended.

        Args:
            controller: Shared game state and service dependencies.

        Returns:
            The outcome scene, or this scene while play continues.
        """

        if controller.game_session.game_status == GameStatus.GAME_OVER:
            return self.defeat_scene
        elif controller.game_session.game_status == GameStatus.VICTORY:
            return self.victory_scene
        return self

    def _handle_playing_inputs(
            self,
            user_input: str | None,
            controller: GameContext
            ) -> GameScene:
        """Apply gameplay controls and handle pause or cheat requests.

        Args:
            user_input: Input received during this frame, if any.
            controller: Shared game state and service dependencies.

        Returns:
            The resulting scene.
        """

        if user_input == "KEY_P":
            controller.game_session.switch_status_paused()
            return PausedScene(previous_scene=self)

        elif user_input == "KEY_C":
            controller.game_session.switch_status_paused()
            return CheatScene(previous_scene=self)

        if user_input == "KEY_W":
            controller.game_board.player.set_direction(Direction.NORTH)
        elif user_input == "KEY_S":
            controller.game_board.player.set_direction(Direction.SOUTH)
        elif user_input == "KEY_A":
            controller.game_board.player.set_direction(Direction.WEST)
        elif user_input == "KEY_D":
            controller.game_board.player.set_direction(Direction.EAST)

        return self

    def _update_player_and_timers(
            self,
            elapsed_time: float,
            controller: GameContext) -> None:
        """Advance session timers and player movement.

        Args:
            elapsed_time: Time elapsed since the previous update, in seconds.
            controller: Shared game state and service dependencies.
        """

        controller.game_session.update_timers(elapsed_time)
        controller.game_board.player.update(
            elapsed_time * controller.game_session.speed_multiplier)

    def _get_player_position(self, controller: GameContext) -> Vector2D:
        """Return the player's current grid position.

        Args:
            controller: Shared game state and service dependencies.

        Returns:
            The player's grid coordinates.
        """
        return Vector2D(
            y=controller.game_board.player.current_pos_y,
            x=controller.game_board.player.current_pos_x
        )

    def _get_player_pixel_position(
            self, controller: GameContext) -> tuple[float, float]:
        """Return the player's current pixel coordinates.

        Args:
            controller: Shared game state and service dependencies.

        Returns:
            The player's vertical and horizontal pixel positions.
        """
        player = controller.game_board.player
        return player.move_pixel_y, player.move_pixel_x

    def _find_nearby_position(
            self,
            positions: set[Vector2D],
            player_pixel_pos: tuple[float, float]
            ) -> Vector2D | None:
        """Find a grid position close to the player's pixel position.

        Args:
            positions: Candidate grid positions.
            player_pixel_pos: Player's vertical and horizontal pixel values.

        Returns:
            A nearby candidate, or None if no candidate is close enough.
        """
        player_y, player_x = player_pixel_pos
        center_y = round(player_y)
        center_x = round(player_x)
        if abs(player_y - center_y) <= 0.5 and abs(player_x - center_x) <= 0.5:
            for position in positions:
                if position.y == center_y and position.x == center_x:
                    return position
        return None

    def handle_pacgums(self, controller: GameContext,
                       player_pixel_pos: tuple[float, float]) -> bool:
        """Consume a regular pacgum at the player's position.

        Args:
            controller: Shared game state and service dependencies.
            player_pixel_pos: Player's vertical and horizontal pixel values.

        Returns:
            Whether a pacgum was consumed.
        """
        pacgum_pos = self._find_nearby_position(
            controller.game_board.pacgum_pos, player_pixel_pos)
        if pacgum_pos is not None:
            controller.game_board.pacgum_pos.remove(pacgum_pos)
            controller.game_session.consume_pacgum()
            controller.view.playing_view.erase_pacgum(
                pacgum_pos.y, pacgum_pos.x)
            return True
        return False

    def handle_super_pacgums(self, controller: GameContext,
                             player_pixel_pos: tuple[float, float]) -> bool:
        """Consume a super pacgum and frighten active ghosts.

        Args:
            controller: Shared game state and service dependencies.
            player_pixel_pos: Player's vertical and horizontal pixel values.

        Returns:
            Whether a super pacgum was consumed.
        """
        super_pacgum_pos = self._find_nearby_position(
            controller.game_board.super_pacgums_pos, player_pixel_pos)
        if super_pacgum_pos is not None:
            controller.game_board.super_pacgums_pos.remove(super_pacgum_pos)
            controller.game_session.consume_super_pacgum()
            controller.view.playing_view.erase_pacgum(
                super_pacgum_pos.y, super_pacgum_pos.x)
            for ghost in controller.game_board.ghosts.values():
                if ghost.state != GhostState.EATEN:
                    ghost.state = GhostState.FRIGHTENED
            return True

        return False

    def _handle_consumables(
            self,
            controller: GameContext,
            player_pixel_pos: tuple[float, float]) -> bool:
        """Check for and consume a pacgum near the player.

        Args:
            controller: Shared game state and service dependencies.
            player_pixel_pos: Player's vertical and horizontal pixel values.

        Returns:
            Whether a consumable was collected.
        """

        return (self.handle_super_pacgums(
                    controller, player_pixel_pos) or
                self.handle_pacgums(
                    controller, player_pixel_pos))

    def _handle_ghosts_and_collisions(
            self,
            controller: GameContext,
            player_pixel_pos: tuple[float, float],
            elapsed_time: float) -> None:
        """Update ghosts and resolve collisions with the player.

        Args:
            controller: Shared game state and service dependencies.
            player_pixel_pos: Player's vertical and horizontal pixel values.
            elapsed_time: Time elapsed since the previous update, in seconds.
        """

        if controller.game_session.power_just_expired:
            for ghost in controller.game_board.ghosts.values():
                if ghost.state != GhostState.EATEN:
                    ghost.state = GhostState.NORMAL

        player = controller.game_board.player

        for ghost in controller.game_board.ghosts.values():
            if not controller.game_session.cheat_mode.freeze:
                ghost.update(elapsed_time)

            same_position = (
                abs(player.move_pixel_y - ghost.move_pixel_y) < 0.5
                and abs(player.move_pixel_x - ghost.move_pixel_x) < 0.5
            )

            if same_position:
                if (controller.game_session.active_power and
                        ghost.state == GhostState.FRIGHTENED):

                    ghost.get_eaten()
                    controller.game_session.consume_ghost()

                elif ghost.state == GhostState.NORMAL:
                    if not controller.game_session.cheat_mode.invincibility:
                        player.start_death_animation()
                        return

    def _check_update_level(self, controller: GameContext) -> None:
        """Load the current level or rebuild the board after progression.

        Args:
            controller: Shared game state and service dependencies.
        """

        if self.current_level_index is None:
            self.current_level_index = controller.game_session.level_index
            controller.view.load_maze(controller.game_board)
            return

        session_level = controller.game_session.level_index
        if session_level > self.current_level_index:
            controller.game_board = controller.level_manager.build_level()
            controller.view.playing_view.clear_all_layers()
            controller.game_session.time_remaining = float(
                controller.game_session.settings.level_max_time)
            controller.view.load_maze(controller.game_board)
            self.current_level_index = session_level

    def render(self, controller: GameContext) -> None:
        """Draw the current game state.

        Args:
            controller: Shared game state and service dependencies.
        """
        controller.view.draw_game(
            controller.game_board, controller.game_session)
