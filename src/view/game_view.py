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
    """Coordinate rendering for game screens and menus."""

    def __init__(
            self,
            screen_width: int,
            screen_height: int,
            sprite_sheet: SpriteSheetsManager,
            window: pygame.Surface) -> None:
        """Create views for each game screen.

        Args:
            screen_width: Display width in pixels.
            screen_height: Display height in pixels.
            sprite_sheet: Sprite assets used by the views.
            window: Display surface to draw on.
        """
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
        """Load the current board into the playing view.

        Args:
            game_board: Board whose maze should be prepared.
        """
        self.playing_view.load_level(game_board)

    def clear_window(self) -> None:
        """Clear the display to black."""
        self.window.fill((0, 0, 0))

    def draw_game(
            self, game_board: GameBoard, game_session: GameSession) -> None:
        """Render the active game state.

        Args:
            game_board: Current game board.
            game_session: Current session state.
        """
        self.playing_view.render(game_board, game_session)

    def draw_menu(self) -> None:
        """Render the main menu."""
        self.menu.render()

    def draw_highscores(
            self, scores: list[HighScore]) -> None:
        """Render the supplied high scores.

        Args:
            scores: High scores to display.
        """
        self.highscores.render(scores)

    def draw_victory(self, score: int) -> None:
        """Render the victory screen for a score.

        Args:
            score: Final score to display.
        """
        self.victory.render(score)

    def draw_defeat(self, score: int) -> None:
        """Render the defeat screen for a score.

        Args:
            score: Final score to display.
        """
        self.defeat.render(score)

    def draw_instruction(self) -> None:
        """Render the instructions screen."""
        self.instruction.render()

    def draw_paused(self) -> None:
        """Render the paused screen."""
        self.paused.render()

    def draw_cheat(self) -> None:
        """Render the cheat-mode screen."""
        self.cheat.render()

    def handle_events(self) -> str | None:
        """Return the last mapped key action from pending events.

        Returns:
            The mapped key action, or None when no key was pressed.
        """
        key: str | None = None
        for event in mlx.get_events():
            action = mlx.get_key_pressed(event)
            if action is not None:
                key = action
        return key
