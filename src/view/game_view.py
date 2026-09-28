import pygame
from . import mlx_wrapper as mlx
from .sprite_sheet_manager import SpriteSheetManager
from .maze_creator import Maze
from .pacgum import Pacgums
from ..model import GameBoard, GameSession


class GameView:
    def __init__(
            self,
            sprite_sheet: SpriteSheetManager,
            window: pygame.Surface) -> None:

        self.sprite_sheet = sprite_sheet
        self.window = window
        self.maze: Maze | None = None

    def load_maze(self, game_board: GameBoard) -> None:
        self.maze = Maze(game_board, self.sprite_sheet, self.window)
        self.pacgums = Pacgums(game_board, self.sprite_sheet, self.window)

    def clear_window(self) -> None:
        self.window.fill((0, 0, 0))
        mlx.update_window()

    def draw_game(
            self,
            game_board: GameBoard,
            game_session: GameSession) -> None:

        if self.maze is not None:
            buffer = mlx.to_buffer(self.window)
            dest_width = self.window.get_width()
            dest_height = self.window.get_height()
            self.maze.render(buffer, dest_width)
            self.pacgums.render(buffer, dest_width)
            pygame.surfarray.blit_array(
                self.window,
                buffer.reshape((dest_height, dest_width)).T)
            mlx.update_window()

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

    def close(self) -> None:
        mlx.quit_window()
