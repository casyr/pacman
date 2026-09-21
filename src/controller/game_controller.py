import time
from enum import Enum, auto
from ..parsing import ConfigParser
from ..model import (
    GameSession,
    LevelBuilder,
    HighScoreManager,
    HighScore,
    GameBoard,
    GameStatus,
)
from ..utils import JsonModelLoader
from ..shared import GhostState, Vector2D


class GameMenuState(Enum):
    MENU = auto()
    PLAYING = auto()
    VICTORY = auto()
    DEFEAT = auto()
    ENTER_HIGHSCORE = auto()
    EXIT = auto()


class GameController:
    def __init__(self, config_path: str):
        loader = ConfigParser(config_path)
        self.game_config = loader.load()

        json_loader = JsonModelLoader(self.game_config.highscore_filename)
        self.highscore_manager = HighScoreManager(json_loader)

        self.game_session = GameSession(self.game_config)
        self.level_manager = LevelBuilder(self.game_session)

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
            elif self.state == GameMenuState.ENTER_HIGHSCORE:
                self._run_highscore_state()
            processing_time = time.perf_counter() - current_time
            time_to_sleep = self.frame_duration - processing_time
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)
                self.last_time = time.perf_counter()

    def get_input(self) -> str:
        choix = input(
            "Choices (1: Start, 2: Highscores, 3:Instruction 4: Exit) : ")
        if choix == "1":
            return "START_KEY"
        elif choix == "2":
            return "HIGHSCORES_KEY"
        elif choix == "3":
            return "INSTRUCTION_KEY"
        elif choix == "4":
            return "EXIT_KEY"
        return ""

    def get_input_move(self) -> str:
        choix = input(
            "Choices (w: up, s: down, right:d left: a) : ")
        if choix == "w":
            return "KEY_UP"
        elif choix == "s":
            return "KEY_DOWN"
        elif choix == "d":
            return "KEY_RIGHT"
        elif choix == "a":
            return "KEY_LEFT"
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

        self.game_session.update_timers(elapsed_time)
        self.game_board.player.update(elapsed_time)
        for ghost in self.game_board.ghosts:
            ghost.update(elapsed_time)

        player_pos = Vector2D(
            y=self.game_board.player.current_pos_y,
            x=self.game_board.player.current_pos_x
        )
        print(player_pos)
        if player_pos in self.game_board.pacgum_pos:
            print("miam")
            self.game_board.pacgum_pos.remove(player_pos)
            self.game_session.consume_pacgum()

        if player_pos in self.game_board.super_pacgums_pos:
            print("miam")
            self.game_board.super_pacgums_pos.remove(player_pos)
            self.game_session.consume_super_pacgum()
            for ghost in self.game_board.ghosts:
                if ghost.state != GhostState.EATEN:
                    ghost.state = GhostState.FRIGHTENED

        if not self.game_session.active_power:
            for ghost in self.game_board.ghosts:
                if ghost.state == GhostState.FRIGHTENED:
                    ghost.state = GhostState.NORMAL

        for ghost in self.game_board.ghosts:
            ghost_pos = ghost.current_pos_y, ghost.current_pos_x
            if player_pos == ghost_pos:
                if (self.game_session.active_power and
                        ghost.state == GhostState.FRIGHTENED):
                    ghost.get_eaten()
                    self.game_session.consume_ghost()

                elif ghost.state == GhostState.NORMAL:
                    print("found you")
                    self.game_session.lose_life()
                    if self.game_session.game_status == GameStatus.PLAYING:
                        self.game_board.player.respawn()

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
            if HighScore._handle_player_names(player_name):
                is_valid = True
            error_name_score: str = f"{player_name} only 10 letters or digits"
            print(error_name_score)
        if player_name:
            self.highscore_manager.update_score(
                player_name, self.game_session.score)
            self.state = GameMenuState.MENU
