import pygame
from . import mlx_wrapper as mlx
from .sprite_sheet_manager import SpriteSheetsManager
from .maze_creator import Maze
from .pacgum import Pacgums
from ..model import GameBoard, GameSession


class GameView:
    def __init__(
            self,
            sprite_sheet: SpriteSheetsManager,
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
            dest_width = self.window.get_width()
            dest_height = self.window.get_height()
            self.render_image = mlx.new_image(dest_width, dest_height).convert_alpha()
            buffer = mlx.to_buffer(self.render_image)

            self.maze.render(buffer, dest_width)
            self.pacgums.render(buffer, dest_width)
            del buffer
            mlx.blit_img(self.render_image, self.window, (0, 0))
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
