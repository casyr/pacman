from pygame import Surface
from . import mlx_wrapper as mlx
from .maze_creator import Maze
from .pacgum import Pacgums
from .entities_view import (
        BlinkyView,
        ClydeView,
        InkyView,
        PacmanView,
        PinkyView
    )
from .menu import BaseMenuView
from .session_view import SessionView
from ..model import GameBoard, GameSession
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from .displayer_utils import DisplayerUtils


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
        self.ghosts: list[BlinkyView | PinkyView | InkyView | ClydeView] = []


        self.maze_img: Surface | None = None
        self.pacgum_img: Surface | None = None
        self.pacman_img: Surface | None = None

        self.utils = DisplayerUtils()

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
        self.ghosts = [
            BlinkyView(game_board, self.sprite_sheets, self.window),
            PinkyView(game_board, self.sprite_sheets, self.window),
            InkyView(game_board, self.sprite_sheets, self.window),
            ClydeView(game_board, self.sprite_sheets, self.window),
        ]
        self._render_maze_layer()
        self._render_pacgums_layer()

    def update_pacgums(self) -> None:
        self._render_pacgums_layer()

    def _render_maze_layer(self) -> None:
        if self.maze is None or self.game_board is None:
            return
        self.maze_img.fill((0, 0, 0, 0))
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
            if self.session_info is not None:
                self.session_info.render(
                        dynamic_buffer,
                        game_session
                    )

            del dynamic_buffer

        mlx.blit_img(self.dynamic_img, self.window, (0, 0))
        mlx.update_window()
    # def render(self, is_maze_updated: bool,
    #            is_pacgum_updated: bool,
    #            game_board: GameBoard,
    #            game_session: GameSession) -> None:

    #     start = time.time()

    #     if is_maze_updated or self.maze_img is None:
    #         print("ici")
    #         self.maze_img = mlx.new_image(self.screen_width,
    #                                       self.screen_height)
    #         self.maze_img = self.maze_img.convert_alpha()
    #         maze_buffer = mlx.to_buffer(self.maze_img, False)
    #         maze = Maze(game_board, self.window,
    #                     self.sprite_sheets)
    #         maze.render(maze_buffer, self.screen_width,
    #                     game_board, self.window)
    #         self.maze_start_x = maze.x_start
    #         self.maze_start_y = maze.y_start
    #         del maze_buffer

    #     mlx.blit_img(self.maze_img, self.window, (self.maze_start_x, self.maze_start_y))

    #     if is_pacgum_updated or self.pacgum_img is None:
    #         print("ici")
    #         self.pacgum_img = mlx.new_image(self.screen_width,
    #                                         self.screen_height)
    #         self.pacgum_img = self.pacgum_img.convert_alpha()
    #         pacgum_buffer = mlx.to_buffer(self.pacgum_img)
    #         pacgum = Pacgums(game_board,
    #                          self.sprite_sheets,
    #                          self.window)
    #         pacgum.render(pacgum_buffer, self.screen_width)

    #         del pacgum_buffer

    #     mlx.blit_img(self.pacgum_img, self.window, (self.maze_start_x, self.maze_start_x))

    #     pacman_width = self.utils.get_tile_size_maze(16, 16, self.screen_width, self.screen_height)
    #     dest_pacman_img = mlx.new_image(pacman_width, pacman_width).convert_alpha()
    #     dest_pacman_buffer = mlx.to_buffer(dest_pacman_img)
    #     pacman = Pacman(game_board, self.sprite_sheets, self.window)
    #     pacman.render(dest_pacman_buffer, pacman_width, game_board,
    #                   self.window)
    #     del dest_pacman_buffer
    #     mlx.blit_img(dest_pacman_img, self.window, (pacman.dest_x, pacman.dest_y))

    #     mlx.update_window()
    #     end = time.time()