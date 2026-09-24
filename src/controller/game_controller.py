import time
import logging
from enum import Enum, auto

from ..model import (
    GameSession,
    GameStatus,
    LevelBuilder,
    HighScoreManager,
    HighScore,
    GameBoard,
)
from ..view import GameView
from ..shared import GhostState, Vector2D

logger = logging.getLogger(__name__)


class GameMenuState(Enum):
    MENU = auto()
    PLAYING = auto()
    VICTORY = auto()
    DEFEAT = auto()
    PAUSED = auto()
    CHEAT_MENU = auto()
    ENTER_HIGHSCORE = auto()
    EXIT = auto()


class GameController:
    def __init__(
            self,
            level_manager: LevelBuilder,
            highscore_manager: HighScoreManager,
            game_session: GameSession,
            game_view: GameView):

        self.level_manager = level_manager
        self.highscore_manager = highscore_manager
        self.game_session = game_session
        self.state = GameMenuState.MENU
        self.game_board: GameBoard = self.level_manager.build_level()
        self.view = game_view
        self.player_name: str = ""
        self.last_time = time.perf_counter()

        self.target_fps: int = 60
        self.frame_duration: float = 1.0 / self.target_fps

    def run(self) -> None:
        self.view.initialize_graphics()
        # self.view.load_assets()
        while self.state != GameMenuState.EXIT:
            current_time = time.perf_counter()
            elapsed_time = current_time - self.last_time
            self.last_time = current_time

            user_input = self.view.handle_events()

            if self.state == GameMenuState.MENU:
                self._run_menu_state(user_input)
            elif self.state == GameMenuState.PLAYING:
                self._run_playing_state(elapsed_time, user_input)
            elif self.state is GameMenuState.VICTORY:
                self._run_game_victory_state(user_input)
            elif self.state is GameMenuState.DEFEAT:
                self._run_game_over_state(user_input)
            elif self.state == GameMenuState.PAUSED:
                self._run_paused_state(user_input)
            elif self.state == GameMenuState.CHEAT_MENU:
                self._run_cheat_menu_state(user_input)
            elif self.state == GameMenuState.ENTER_HIGHSCORE:
                self._run_highscore_state(user_input)

            processing_time = time.perf_counter() - self.last_time
            time_to_sleep = self.frame_duration - processing_time
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)
        self.view.close()

    def _run_menu_state(self, user_input: str | None) -> None:
        # self.view.draw_main_menu()
        if user_input == "KEY_1":
            self.game_session.reset_level_data()
            self.game_board = self.level_manager.build_level()
            self.state = GameMenuState.PLAYING
        elif user_input == "KEY_2":
            scores = self.highscore_manager.scores
            logger.debug(scores)
            # self.view.draw_highscores(self.highscore_manager.scores)
        elif user_input == "KEY_3":
            # self.view.draw_instructions()
            pass
        elif user_input == "KEY_4":
            self.state = GameMenuState.EXIT

    def _check_game_end_conditions(self) -> bool:
        if self.game_session.game_status == GameStatus.GAME_OVER:
            self.state = GameMenuState.DEFEAT
            return True
        elif self.game_session.game_status == GameStatus.VICTORY:
            self.state = GameMenuState.VICTORY
            return True
        return False

    def _handle_playing_inputs(self, user_input: str | None) -> None:
        if user_input == "KEY_P":
            self.state = GameMenuState.PAUSED
            self.game_session.switch_status_paused()
            # self.view.draw_pause_menu()
        elif user_input == "KEY_C":
            self.state = GameMenuState.CHEAT_MENU
            self.game_session.switch_status_paused()
            # self.view.draw_cheat_menu()
        elif user_input == "KEY_T":
            self.state = GameMenuState.VICTORY

        if user_input == "KEY_W":
            self.game_board.player.set_direction(-1, 0)
        elif user_input == "KEY_S":
            self.game_board.player.set_direction(1, 0)
        elif user_input == "KEY_A":
            self.game_board.player.set_direction(0, -1)
        elif user_input == "KEY_D":
            self.game_board.player.set_direction(0, 1)

    def _update_player_and_timers(self, elapsed_time: float) -> None:
        self.game_session.update_timers(elapsed_time)
        self.game_board.player.update(
            elapsed_time * self.game_session.speed_multiplier)

    def _handle_consumables(self, player_pos: Vector2D) -> None:
        if player_pos in self.game_board.pacgum_pos:
            logger.debug("miam")
            self.game_board.pacgum_pos.remove(player_pos)
            self.game_session.consume_pacgum()

        if player_pos in self.game_board.super_pacgums_pos:
            logger.debug("SUPER miam")
            self.game_board.super_pacgums_pos.remove(player_pos)
            self.game_session.consume_super_pacgum()
            for ghost in self.game_board.ghosts:
                if ghost.state != GhostState.EATEN:
                    ghost.state = GhostState.FRIGHTENED

    def _handle_ghosts_and_collisions(
            self, player_pos: Vector2D, elapsed_time: float) -> None:

        if self.game_session.cheat_mode.freeze:
            return

        for ghost in self.game_board.ghosts:
            ghost.update(elapsed_time)
            ghost_pos = Vector2D(ghost.current_pos_y, ghost.current_pos_x)

            if self.game_session.power_just_expired:
                ghost.state = GhostState.NORMAL

            if player_pos == ghost_pos:
                if (self.game_session.active_power and
                        ghost.state == GhostState.FRIGHTENED):
                    ghost.get_eaten()
                    logger.debug("Ghost miam")
                    self.game_session.consume_ghost()

                elif ghost.state == GhostState.NORMAL:
                    logger.debug("found you")
                    if self.game_session.lose_life():
                        self.game_board.player.respawn()
                        ghost.respawn()

    def _run_playing_state(
            self,
            elapsed_time: float,
            user_input: str | None) -> None:

        if self._check_game_end_conditions():
            return

        self._handle_playing_inputs(user_input)
        self._update_player_and_timers(elapsed_time)

        player_pos = Vector2D(
            y=self.game_board.player.current_pos_y,
            x=self.game_board.player.current_pos_x
        )
        logger.debug(f'player_pos : {player_pos}')
        self._handle_consumables(player_pos)
        self._handle_ghosts_and_collisions(player_pos, elapsed_time)
        # self.view.draw_game(self.game_board, self.game_session)

    def _run_game_victory_state(self, user_input: str | None) -> None:
        logger.debug(f"Victory ! Final Score : {self.game_session.score}")
        # self.view.draw_victory_screen(self, self.game_session.score)
        self.state = GameMenuState.ENTER_HIGHSCORE

    def _run_game_over_state(self, user_input: str | None) -> None:
        logger.debug(f"Game Over ! Final Score : {self.game_session.score}")
        # self.view.draw_game_over_screen(self, self.game_session.score)
        self.state = GameMenuState.ENTER_HIGHSCORE

    def _run_instruction_state(self, user_input: str | None) -> None:
        # self.view.draw_instruction(self)
        if user_input == "KEY_1":
            self.state = GameMenuState.MENU

    def _run_highscore_state(self, user_input: str | None) -> None:
        char: str | None = None
        print(f"player {self.player_name}")
        # self.view.draw_enter_name_screen(self)
        if user_input is None:
            return
        if user_input == "KEY_RETURN":
            print("HE SUIS ICI")
            if not HighScore._handle_player_names(self.player_name.strip()):
                error_name_score: str = (f"{self.player_name}"
                                         "only 10 letters or digits")
                print(error_name_score)
                self.player_name = ""
            else:
                self.highscore_manager.update_score(
                    self.player_name, self.game_session.score)
                self.game_session.reset_level_data()
                self.state = GameMenuState.MENU
        elif user_input.startswith("KEY_"):
            char = user_input[4:].lower()
            self.player_name += char
            print(f"player {self.player_name}")
        elif user_input.startswith("CHAR_"):
            char = user_input[5:]
            self.player_name += char

    def _run_paused_state(self, pause_choice: str | None) -> None:
        # self.view.draw_pause_menu()
        if pause_choice == "KEY_1":
            self.state = GameMenuState.PLAYING
        elif pause_choice == "KEY_2":
            self.state = GameMenuState.MENU
        self.game_session.switch_status_paused()

    def _run_cheat_menu_state(self, cheat_choice: str | None) -> None:
        # self.view.draw_cheat_menu()
        print(self.game_session.time_remaining)
        if cheat_choice == "KEY_1":
            self.game_session.switch_invincibility()
            print("Invincibility is now"
                  f"{self.game_session.cheat_mode.invincibility}")

        elif cheat_choice == "KEY_2":
            self.game_session.switch_ghost_freeze()
            for ghost in self.game_board.ghosts:
                print(f"x : {ghost.current_pos_x}")
                print(f"y : {ghost.current_pos_y}")
            print(f"Ghost Freeze is now {self.game_session.cheat_mode.freeze}")

        elif cheat_choice == "KEY_3":
            self.game_session.switch_speed_boost()
            print(f"Speed Boost is now {self.game_session.cheat_mode.speed}")

        elif cheat_choice == "KEY_4":
            self.game_session.cheat_extra_lives()
            print(f"Lives remaining: {self.game_session.lives_remaining}")

        elif cheat_choice == "KEY_5":
            self.game_session.cheat_skip_level()
            if self.game_session.game_status == GameStatus.VICTORY:
                self.state = GameMenuState.VICTORY
            else:
                self.game_board = self.level_manager.build_level()
                self.game_session.next_level_data()
                self.state = GameMenuState.PLAYING

        elif cheat_choice == "KEY_6":
            self.game_session.cheat_add_score()
            print(f"You have just found extra point {self.game_session.score}")

        elif cheat_choice == "KEY_C":
            self.game_session.switch_status_paused()
            self.state = GameMenuState.PLAYING
