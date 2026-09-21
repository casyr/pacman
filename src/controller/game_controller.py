import time
from enum import Enum, auto

from ..model import (
    GameSession,
    GameStatus,
    LevelBuilder,
    HighScoreManager,
    HighScore,
    GameBoard,
)

from ..shared import GhostState, Vector2D


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
            game_session: GameSession):

        self.level_manager = level_manager
        self.highscore_manager = highscore_manager
        self.game_session = game_session
        self.state = GameMenuState.MENU
        self.game_board: GameBoard = self.level_manager.build_level()
        # self.view = GameView()

        self.last_time = time.perf_counter()
        self.target_fps: int = 60
        self.frame_duration: float = 1.0 / self.target_fps

    def run(self) -> None:
        # self.view.initialize_graphics()
        # self.view.load_assets()
        while self.state != GameMenuState.EXIT:
            current_time = time.perf_counter()
            elapsed_time = current_time - self.last_time
            self.last_time = current_time

            if self.state == GameMenuState.MENU:
                self._run_menu_state()
            elif self.state == GameMenuState.PLAYING:
                self._run_playing_state(elapsed_time)
            elif self.state is GameMenuState.VICTORY:
                self._run_game_victory_state()
            elif self.state is GameMenuState.DEFEAT:
                self._run_game_over_state()
            elif self.state == GameMenuState.PAUSED:
                self._run_paused_state()
            elif self.state == GameMenuState.CHEAT_MENU:
                self._run_cheat_menu_state()
            elif self.state == GameMenuState.ENTER_HIGHSCORE:
                self._run_highscore_state()
            processing_time = time.perf_counter() - current_time
            time_to_sleep = self.frame_duration - processing_time
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)
                self.last_time = time.perf_counter()

    def get_input(self) -> str:
        choices = input(
            "Choices (1: Start, 2: Highscores, 3:Instruction 4: Exit) : ")
        if choices == "1":
            return "START_KEY"
        elif choices == "2":
            return "HIGHSCORES_KEY"
        elif choices == "3":
            return "INSTRUCTION_KEY"
        elif choices == "4":
            return "EXIT_KEY"
        return ""

    def get_input_move(self) -> str:
        choices = input(
            "Choices (w: up, s: down, right:d left: a  paused: p cheat: c) : ")
        if choices == "w":
            return "KEY_UP"
        elif choices == "s":
            return "KEY_DOWN"
        elif choices == "d":
            return "KEY_RIGHT"
        elif choices == "a":
            return "KEY_LEFT"
        elif choices == "p":
            return "KEY_PAUSED"
        elif choices == "c":
            return "KEY_CHEAT_MENU"
        return ""

    def get_input_paused(self) -> str:
        choices = input("1: Resume, 2: Return to Main Menu : ")
        if choices == "1":
            return "RESUME"
        elif choices == "2":
            return "RETURN MAIN MENU"
        return ""

    def get_input_cheat(self) -> str:
        choices = input("Select a cheat : ")
        if choices == "1":
            return "CHEAT_INVINCIBLE"
        elif choices == "2":
            return "CHEAT_FREEZE"
        elif choices == "3":
            return "CHEAT_SPEED"
        elif choices == "4":
            return "CHEAT_LIFE"
        elif choices == "5":
            return "CHEAT_SKIP"
        elif choices == "6":
            return "RESUME"
        return ""

    def _run_menu_state(self) -> None:
        # self.view.draw_main_menu()
        user_input = self.get_input()
        if user_input == "START_KEY":
            self.state = GameMenuState.PLAYING
            self.game_board = self.level_manager.build_level()
        elif user_input == "HIGHSCORES_KEY":
            scores = self.highscore_manager.scores
            print(scores)
            # self.view.draw_highscores(scores)
        elif user_input == "INSTRUCTIONS_KEY":
            # self.view.draw_instructions()
            pass
        elif user_input == "EXIT_KEY":
            self.state = GameMenuState.EXIT

    def _run_playing_state(self, elapsed_time: float) -> None:
        move_input = self.get_input_move()
        if move_input == "KEY_UP":
            self.game_board.player.set_direction(-1, 0)
        elif move_input == "KEY_DOWN":
            self.game_board.player.set_direction(1, 0)
        elif move_input == "KEY_LEFT":
            self.game_board.player.set_direction(0, -1)
        elif move_input == "KEY_RIGHT":
            self.game_board.player.set_direction(0, 1)
        elif move_input == "KEY_PAUSED":
            self.state = GameMenuState.PAUSED
            self.game_session.switch_status_paused()
        elif move_input == "KEY_CHEAT_MENU":
            self.state = GameMenuState.CHEAT_MENU
            self.game_session.switch_status_paused()
            return

        if self.game_board.player.move_dir != (0, 0):
            self.game_board.player.set_direction(
                self.game_board.player.move_dir.y,
                self.game_board.player.move_dir.x)

        self.game_session.update_timers(elapsed_time)
        self.game_board.player.update(elapsed_time)

        player_pos = Vector2D(
            y=self.game_board.player.current_pos_y,
            x=self.game_board.player.current_pos_x
        )
        print(f'player_pos : {player_pos}')
        if player_pos in self.game_board.pacgum_pos:
            print("miam")
            self.game_board.pacgum_pos.remove(player_pos)
            self.game_session.consume_pacgum()

        if player_pos in self.game_board.super_pacgums_pos:
            print("SUPER miam")
            self.game_board.super_pacgums_pos.remove(player_pos)
            self.game_session.consume_super_pacgum()
            for ghost in self.game_board.ghosts:
                if ghost.state != GhostState.EATEN:
                    ghost.state = GhostState.FRIGHTENED

        for ghost in self.game_board.ghosts:
            ghost.update(elapsed_time)
            ghost_pos = Vector2D(ghost.current_pos_y, ghost.current_pos_x)

            if self.game_session.power_just_expired:
                ghost.state = GhostState.NORMAL

            if player_pos == ghost_pos:
                if (self.game_session.active_power and
                        ghost.state == GhostState.FRIGHTENED):
                    ghost.get_eaten()
                    print("Ghost miam")
                    self.game_session.consume_ghost()

                elif ghost.state == GhostState.NORMAL:
                    print("found you")
                    self.game_session.lose_life()
                    if self.game_session.game_status == GameStatus.PLAYING:
                        self.game_board.player.respawn()
                        ghost.respawn()
                        print(ghost_pos)

        if self.game_session.game_status == GameStatus.GAME_OVER:
            self.state = GameMenuState.DEFEAT
        elif self.game_session.game_status == GameStatus.VICTORY:
            self.state = GameMenuState.VICTORY

    def _run_game_victory_state(self) -> None:
        print(f"Victory ! Final Score : {self.game_session.score}")
        self.state = GameMenuState.ENTER_HIGHSCORE

    def _run_game_over_state(self) -> None:
        print(f"Game Over ! Final Score : {self.game_session.score}")
        self.state = GameMenuState.ENTER_HIGHSCORE

    def _run_instruction_state(self) -> None:
        pass

    def _run_highscore_state(self) -> None:
        is_valid = False
        while not is_valid:
            player_name = input("Pseudo : ")
            if not HighScore._handle_player_names(player_name):
                error_name_score: str = (f"{player_name}"
                                         "only 10 letters or digits")
                print(error_name_score)
            else:
                is_valid = True
        if player_name:
            self.highscore_manager.update_score(
                player_name, self.game_session.score)
            self.game_session.reset_level_data()
            self.state = GameMenuState.MENU

    def _run_paused_state(self) -> None:
        # self.view.draw_pause_menu()
        pause_choice = self.get_input_paused()
        if pause_choice == "RESUME":
            self.state = GameMenuState.PLAYING
        elif pause_choice == "RETURN MAIN MENU":
            self.state = GameMenuState.MENU
        self.game_session.switch_status_paused()

    def _run_cheat_menu_state(self) -> None:
        # self.view.draw_cheat_menu()
        cheat_choice = self.get_input_cheat()
        if cheat_choice == "CHEAT_INVINCIBLE":
            self.game_session.switch_invincibility()
            print(f"Invincibility is now {
                self.game_session.cheat_mode.invincibility}")

        elif cheat_choice == "CHEAT_FREEZE":
            self.game_session.switch_ghost_freeze()
            print(f"Ghost Freeze is now {self.game_session.cheat_mode.freeze}")

        elif cheat_choice == "CHEAT_SPEED":
            self.game_session.switch_speed_boost()
            print(f"Speed Boost is now {self.game_session.cheat_mode.speed}")

        elif cheat_choice == "CHEAT_LIFE":
            self.game_session.cheat_extra_lives()
            print(f"Lives remaining: {self.game_session.lives_remaining}")

        elif cheat_choice == "CHEAT_SKIP":
            self.game_session.cheat_skip_level()
            if self.game_session.game_status == GameStatus.PLAYING:
                self.game_board = self.level_manager.build_level()
            self.state = GameMenuState.PLAYING

        elif cheat_choice == "RESUME":
            self.game_session.switch_status_paused()
            self.state = GameMenuState.PLAYING
