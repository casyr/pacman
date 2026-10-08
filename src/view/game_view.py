import pygame
from . import mlx_wrapper as mlx
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from .menu_main import Menu
from .menu_highscore import HighScoresView
from .menu_victory import VictoryView
from .menu_defeat import DefeatView
from .menu_instructions import InstructionsView
from .menu_paused import PausedView
from .menu_cheat import CheatView
from ..model import GameBoard, GameSession
from ..model import HighScore
from .playing_view import PlayingView


class GameView:

    def __init__(
            self,
            screen_width: int,
            screen_height: int,
            sprite_sheet: SpriteSheetsManager,
            window: pygame.Surface) -> None:
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.sprite_sheet = sprite_sheet
        self.window = window
        self.playing_view: PlayingView = PlayingView(
            screen_width, screen_height, window, sprite_sheet)
        self.menu: Menu = Menu(
            screen_width, screen_height, window, sprite_sheet)
        self.highscores: HighScoresView = HighScoresView(
            screen_width, screen_height, window, sprite_sheet)
        self.victory: VictoryView = VictoryView(
            screen_width, screen_height, window, sprite_sheet)
        self.defeat: DefeatView = DefeatView(
            screen_width, screen_height, window, sprite_sheet)
        self.instruction: InstructionsView = InstructionsView(
            screen_width, screen_height, window, sprite_sheet)
        self.paused: PausedView = PausedView(
            screen_width, screen_height, window, sprite_sheet)
        self.cheat: CheatView = CheatView(
            screen_width, screen_height, window, sprite_sheet)

    def load_maze(self, game_board: GameBoard) -> None:
        self.playing_view.load_level(game_board)

    def clear_window(self) -> None:
        self.window.fill((0, 0, 0))

    def draw_game(
            self, game_board: GameBoard, game_session: GameSession) -> None:

        self.playing_view.render(game_board, game_session)

    def draw_menu(self) -> None:
        self.menu.render()

    def draw_highscores(
            self, scores: list[HighScore]) -> None:
        self.highscores.render(scores)

    def draw_victory(self, score: int) -> None:
        self.victory.render(score)

    def draw_defeat(self, score: int) -> None:
        self.defeat.render(score)

    def draw_instruction(self) -> None:
        self.instruction.render()

    def draw_paused(self) -> None:
        self.paused.render()

    def draw_cheat(self) -> None:
        self.cheat.render()

    def handle_events(self) -> str | None:
        key: str | None = None
        for event in mlx.get_events():
            action = mlx.get_key_pressed(event)
            if action is not None:
                key = action
        return key
