from .maze_creator import Maze
from .pacgum import Pacgums
from . import mlx_wrapper as mlx
from ..model import GameBoard, GameSession
from pygame import Surface
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from .game_view import GameView
from .entities import Pacman


class PlayingView(GameView):

    def __init__(self, game_board: GameBoard, game_session: GameSession,
                 is_updated: bool, screen_width: int, screen_height: int,
                 window: Surface, sprite_sheet: SpriteSheetsManager):
        self.game_board = game_board
        self.game_session = game_session
        self.is_updated = is_updated
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window = window
        self.sprite_sheets = sprite_sheet
        self.maze_img = mlx.new_image(self.screen_width, self.screen_height)
        self.maze_img = self.maze_img.convert_alpha()
        self.maze_buffer = mlx.to_buffer(self.maze_img, False)

    def render(self, is_updated: bool) -> None:

        if is_updated:
            maze = Maze(self.game_board,
                        self.sprite_sheets,
                        self.window)
            dest_width = self.window.get_width()

            # mlx.clear_window(self.window)

            maze.render(self.maze_buffer, dest_width, self.game_board,
                        self.window)

        # mlx.clear_window(self.window)

        pacgum = Pacgums(self.game_board,
                         self.sprite_sheets,
                         self.window)
        del self.maze_buffer
        mlx.blit_img(self.maze_img, self.window, (0, 0))

        self.pacgum_img = mlx.new_image(self.screen_width, self.screen_height)
        self.pacgum_img = self.pacgum_img.convert_alpha()
        self.pacgum_buffer = mlx.to_buffer(self.pacgum_img)
        pacgum.render(self.pacgum_buffer, self.screen_width)
        del self.pacgum_buffer
        mlx.blit_img(self.pacgum_img, self.window, (0, 0))
        # mlx.update_window()

        pacman = Pacman(self.game_board, self.sprite_sheets, self.window)
        self.pacman_img = mlx.new_image(self.screen_width, self.screen_height)
        self.pacman_img = self.pacman_img.convert_alpha()
        self.pacman_buffer = mlx.to_buffer(self.pacman_img)
        pacman.render(self.pacman_buffer, self.screen_width, self.game_board,
                      self.window)
        del self.pacman_buffer

        mlx.blit_img(self.pacman_img, self.window, (0, 0))

        mlx.update_window()
