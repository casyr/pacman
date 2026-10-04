from .maze_creator import Maze
from .pacgum import Pacgums
from . import mlx_wrapper as mlx
from ..model import GameBoard, GameSession
from pygame import Surface
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from .entities import BlinkyView, ClydeView, InkyView, PacmanView, PinkyView


class PlayingView:

    def __init__(self, screen_width: int, screen_height: int,
                 window: Surface, sprite_sheet: SpriteSheetsManager):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window = window
        self.sprite_sheets = sprite_sheet
        self.game_board: GameBoard | None = None
        self.maze: Maze | None = None
        self.pacgums: Pacgums | None = None
        self.pacman: PacmanView | None = None
        self.ghosts: list[BlinkyView | PinkyView | InkyView | ClydeView] = []

        self.maze_img = mlx.new_image(
            self.screen_width, self.screen_height).convert_alpha()
        self.commestible_img = mlx.new_image(
            self.screen_width, self.screen_height).convert_alpha()
        self.dynamic_img = mlx.new_image(
            self.screen_width, self.screen_height).convert_alpha()

    def load_level(self, game_board: GameBoard) -> None:
        self.game_board = game_board
        self.maze = Maze(game_board, self.window, self.sprite_sheets)
        self.pacgums = Pacgums(
            game_board,
            self.sprite_sheets,
            self.window,
        )
        self.pacman = PacmanView(game_board, self.sprite_sheets, self.window)
        self.ghosts = [
            BlinkyView(game_board, self.sprite_sheets, self.window),
            PinkyView(game_board, self.sprite_sheets, self.window),
            InkyView(game_board, self.sprite_sheets, self.window),
            ClydeView(game_board, self.sprite_sheets, self.window),
        ]
        self._render_maze_layer()
        self._render_pacgums_layer()

    def _render_maze_layer(self) -> None:
        if self.maze is None or self.game_board is None:
            return
        self.maze_img.fill((0, 0, 0, 0))
        maze_buffer = mlx.to_buffer(self.maze_img)
        self.maze.render(
            maze_buffer,
            self.screen_width,
            self.game_board,
            self.window,
        )
        del maze_buffer

    def _render_pacgums_layer(self) -> None:
        if self.pacgums is None:
            return

        self.commestible_img.fill((0, 0, 0, 0))
        pacgums_buffer = mlx.to_buffer(self.commestible_img)
        self.pacgums.render(pacgums_buffer, self.screen_width)
        del pacgums_buffer

    def update_pacgums(self) -> None:
        self._render_pacgums_layer()

    def render(self, game_board: GameBoard,
               game_session: GameSession) -> None:
        mlx.blit_img(self.maze_img, self.window, (0, 0))
        mlx.blit_img(self.commestible_img, self.window, (0, 0))

        if self.pacman is not None:
            self.dynamic_img.fill((0, 0, 0, 0))
            dynamic_buffer = mlx.to_buffer(self.dynamic_img)
            self.pacman.render(
                dynamic_buffer,
                self.screen_width,
                game_board,
                self.window,
            )
            for ghost in self.ghosts:
                ghost.render(
                    dynamic_buffer,
                    self.screen_width,
                    game_board,
                    self.window,
                )
            del dynamic_buffer

        mlx.blit_img(self.dynamic_img, self.window, (0, 0))

        mlx.update_window()
