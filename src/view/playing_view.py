from pygame import Surface
from . import mlx_wrapper as mlx
from .maze_creator import Maze
from .pacgum import Pacgums
from .entities_view import GhostView, PacmanView

from .menu import BaseMenuView
from .session_view import SessionView
from ..model import GameBoard, GameSession
from ..parsing.sprite_sheet_manager import SpriteSheetsManager


class PlayingView(BaseMenuView):

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
        self.session_info: SessionView | None = None
        self.ghostView = GhostView | None

        self.maze_img = mlx.new_image(
            self.screen_width, self.screen_height)

        self.commestible_img = mlx.new_image(
            self.screen_width, self.screen_height).convert_alpha()
        # self.commestible_img.set_colorkey((0, 0, 0))
        self.dynamic_img = mlx.new_image(
            self.screen_width, self.screen_height).convert_alpha()
        # self.dynamic_img.set_colorkey((0, 0, 0))

    def load_level(self, game_board: GameBoard) -> None:
        self.game_board = game_board
        self.maze = Maze(game_board, self.window, self.sprite_sheets)
        self.pacgums = Pacgums(
            game_board,
            self.sprite_sheets,
            self.window,
        )
        self.pacman = PacmanView(game_board, self.sprite_sheets, self.window)
        self.session_info = SessionView(
            self.screen_width,
            self.screen_height,
            self.window,
            self.sprite_sheets
        )
        self.ghosts = GhostView(game_board,
                                self.sprite_sheets,
                                self.window)
        self._render_maze_layer()
        self._render_pacgums_layer()

    def update_pacgums(self) -> None:
        self._render_pacgums_layer()

    def _render_maze_layer(self) -> None:
        if self.maze is None or self.game_board is None:
            return
        # mlx.clear_window(self.dynamic_img)
        maze_buffer = mlx.to_buffer(self.maze_img, False)
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

        mlx.clear_window(self.commestible_img)
        pacgums_buffer = mlx.to_buffer(self.commestible_img, True)
        self.pacgums.render(pacgums_buffer, self.screen_width)
        del pacgums_buffer

    def render(self, game_board: GameBoard,
               game_session: GameSession) -> None:

        mlx.clear_window(self.dynamic_img)
        mlx.blit_img(self.maze_img, self.window, (0, 0))
        mlx.blit_img(self.commestible_img, self.window, (0, 0))

        # start = time.time()

        if self.pacman is None:
            return
        dynamic_buffer = mlx.to_buffer(self.dynamic_img, True)
        self.pacman.render(
                           dynamic_buffer,
                           self.screen_width,
                           game_board)
        self.ghosts.render(dynamic_buffer,
                           self.screen_width,
                           game_board)
        if self.session_info is not None:
            self.session_info.render(
                    dynamic_buffer,
                    game_session
                )

        del dynamic_buffer

        mlx.blit_img(self.dynamic_img, self.window, (0, 0))
        mlx.update_window()

        # end = time.time()
        # print(f"{((end - start))}")
