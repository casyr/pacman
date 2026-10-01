import pygame
from . import mlx_wrapper as mlx
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from .maze_creator import Maze
from .pacgum import Pacgums
from .menu_view import Menu
from .menu_highscore import HighScoresView
from ..model import GameBoard, GameSession
from ..model import HighScore


class GameView:
    def __init__(
            self,
            sprite_sheet: SpriteSheetsManager,
            window: pygame.Surface) -> None:

        self.sprite_sheet = sprite_sheet
        self.window = window
        self.maze: Maze | None = None
        self.menu: Menu | None = None
        self.highscores: HighScoresView | None = None
        self._cached_buffer_menu: pygame.Surface | None = None

    def load_maze(self, game_board: GameBoard) -> None:
        self.maze = Maze(game_board, self.sprite_sheet, self.window)
        self.pacgums = Pacgums(game_board, self.sprite_sheet, self.window)

    def clear_window(self) -> None:
        self.window.fill((0, 0, 0))

    def draw_game(
            self,
            game_board: GameBoard,
            game_session: GameSession) -> None:

        if self.maze is not None:
            dest_width = self.window.get_width()
            dest_height = self.window.get_height()
            render_image = mlx.new_image(dest_width,
                                         dest_height).convert_alpha()
            buffer = mlx.to_buffer(render_image)
            self.maze.render(buffer, dest_width)
            self.pacgums.render(buffer, dest_width)
            del buffer
            mlx.blit_img(render_image, self.window, (0, 0))
            mlx.update_window()

    def _create_cache_menu(
            self,
            dest_width: int,
            dest_height: int) -> pygame.Surface:

        if self.menu is None:
            self.menu = Menu(
                self.sprite_sheet, self.window, dest_width, dest_height)
        if self._cached_buffer_menu is None:
            self._cached_buffer_menu = mlx.new_image(
                dest_width,
                dest_height).convert_alpha()
            buffer = mlx.to_buffer(self._cached_buffer_menu)
            self.menu.render(buffer, dest_width)
            del buffer
        return self._cached_buffer_menu

    def draw_menu(
            self,
            game_board: GameBoard,
            game_session: GameSession) -> None:
        dest_width = self.window.get_width()
        dest_height = self.window.get_height()
        cached_image = self._create_cache_menu(dest_width, dest_height)
        mlx.blit_img(cached_image, self.window, (0, 0))
        mlx.update_window()

    def draw_highscores(
            self, scores: list[HighScore]) -> None:
        dest_width = self.window.get_width()
        dest_height = self.window.get_height()
        if self.highscores is None:
            self.highscores = HighScoresView(
                self.sprite_sheet, self.window, dest_width, dest_height)
        render_image = mlx.new_image(dest_width,
                                     dest_height).convert_alpha()
        buffer = mlx.to_buffer(render_image)
        self.highscores.render(buffer, dest_width, scores)
        del buffer
        mlx.blit_img(render_image, self.window, (0, 0))
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
