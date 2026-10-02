from .maze_creator import Maze
from .pacgum import Pacgums
from . import mlx_wrapper as mlx
from ..model import GameBoard, GameSession
from pygame import Surface
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from .entities import Pacman


class PlayingView:

    def __init__(self, screen_width: int, screen_height: int,
                 window: Surface, sprite_sheet: SpriteSheetsManager):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window = window
        self.sprite_sheets = sprite_sheet

        self.maze_img = mlx.new_image(self.screen_width, self.screen_height)
        self.maze_img = self.maze_img.convert_alpha()
        self.maze_buffer = mlx.to_buffer(self.maze_img, False)

        self.pacgum_img = mlx.new_image(self.screen_width, self.screen_height)
        self.pacgum_img = self.pacgum_img.convert_alpha()
        # self.pacgum_buffer = mlx.to_buffer(self.pacgum_img)

    # def update()

    def render(self, is_maze_updated: bool,
               is_pacgum_updated: bool,
               game_board: GameBoard,
               game_session: GameSession) -> None:

        # if is_maze_updated:
        self.maze_img = mlx.new_image(self.screen_width, self.screen_height)
        self.maze_img = self.maze_img.convert_alpha()
        self.maze_buffer = mlx.to_buffer(self.maze_img, False)
        maze = Maze(game_board, self.window,
                    self.sprite_sheets)

        # mlx.clear_window(self.window)

        maze.render(self.maze_buffer, self.screen_width,
                    game_board, self.window)

        del self.maze_buffer

        mlx.blit_img(self.maze_img, self.window, (0, 0))

        # mlx.clear_window(self.window)

        # if is_pacgum_updated:
        self.pacgum_img = mlx.new_image(self.screen_width, self.screen_height)
        self.pacgum_img = self.pacgum_img.convert_alpha()
        self.pacgum_buffer = mlx.to_buffer(self.pacgum_img)
        pacgum = Pacgums(game_board,
                         self.sprite_sheets,
                         self.window)

        pacgum.render(self.pacgum_buffer, self.screen_width)

        del self.pacgum_buffer

        mlx.blit_img(self.pacgum_img, self.window, (0, 0))
        # mlx.update_window()

        pacman = Pacman(game_board, self.sprite_sheets, self.window)
        self.pacman_img = mlx.new_image(self.screen_width, self.screen_height)
        self.pacman_img = self.pacman_img.convert_alpha()
        self.pacman_buffer = mlx.to_buffer(self.pacman_img)
        pacman.render(self.pacman_buffer, self.screen_width, game_board,
                      self.window)
        del self.pacman_buffer

        mlx.blit_img(self.pacman_img, self.window, (0, 0))

        mlx.update_window()
