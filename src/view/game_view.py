import pygame
from . import mlx_wrapper as mlx
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from ..model import GameBoard, GameSession
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
        self.playing_view = PlayingView(self.screen_width,
                                        self.screen_height,
                                        self.sprite_sheet,
                                        self.window
                                        )

    def handle_events(self) -> str | None:
        key: str | None = None
        for event in mlx.get_events():
            print("Pygame event:", event)
            if event.type == pygame.QUIT:
                return "MOUSE_QUIT"
            action = mlx.get_key_pressed(event)
            if action is not None:
                key = action
        return key

    def draw_game(self, game_board: GameBoard, game_session: GameSession,
                  maze_is_updated: bool) -> None:

        self.playing_view.render(maze_is_updated, game_board, game_session)
