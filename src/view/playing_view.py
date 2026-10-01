from .maze_creator import Maze
from .pacgum import Pacgums
from . import mlx_wrapper as mlx
from ..model import GameBoard, GameSession
from pygame import Surface
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from .entities import Pacman
from .displayer_utils import DisplayerUtils
from ..parsing.sprite_validator import SpriteData, SpriteCoords


class PlayingView:

    def __init__(self, screen_width: int, screen_height: int,
                 sprite_sheet: SpriteSheetsManager, window: Surface):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window = window
        self.sprite_sheets = sprite_sheet

        self.maze_img: Surface | None = None
        self.pacgum_img: Surface | None = None
        self.pacman_img: Surface | None = None

        self.utils = DisplayerUtils()

    def render(self, is_maze_updated: bool,
               is_pacgum_updated: bool,
               game_board: GameBoard,
               game_session: GameSession) -> None:

        dest_img = mlx.new_image(self.screen_width,
                                 self.screen_height).convert_alpha()
        dest_buffer = mlx.to_buffer(dest_img)

        # print("la")

        if is_maze_updated or self.maze_img is None:
            # print("la")
            self.maze_img = mlx.new_image(self.screen_width,
                                          self.screen_height)
            self.maze_img = self.maze_img.convert_alpha()
            maze_buffer = mlx.to_buffer(self.maze_img, False)
            maze = Maze(game_board, self.window,
                        self.sprite_sheets)
            maze.render(maze_buffer, self.screen_width,
                        game_board, self.window)
            maze_coords = SpriteCoords(x=0, y=0, w=self.screen_width, h=self.screen_height)
            maze_sprite = SpriteData(sprite_width=self.screen_width, coords=maze_coords, buffer=maze_buffer)

            self.utils.put_sprite_in_image(dest_buffer,
                                           self.screen_height,
                                           0, 0, self.screen_width,
                                           self.screen_height, maze_sprite)

        if is_pacgum_updated or self.pacgum_img is None:
            print("ici")
            self.pacgum_img = mlx.new_image(self.screen_width,
                                            self.screen_height)
            self.pacgum_img = self.pacgum_img.convert_alpha()
            pacgum_buffer = mlx.to_buffer(self.pacgum_img)
            pacgum = Pacgums(game_board,
                             self.sprite_sheets,
                             self.window)

            pacgum.render(pacgum_buffer, self.screen_width)
            pacgum_coords = SpriteCoords(x=0, y=0, w=self.screen_width, h=self.screen_height)
            pacgum_sprite = SpriteData(sprite_width=self.screen_width, coords=pacgum_coords, buffer=pacgum_buffer)

            self.utils.put_sprite_in_image(dest_buffer,
                                           self.screen_height,
                                           0, 0, self.screen_width,
                                           self.screen_height, pacgum_sprite)

        pacman = Pacman(game_board, self.sprite_sheets, self.window)
        self.pacman_img = mlx.new_image(self.screen_width, self.screen_height)
        self.pacman_img = self.pacman_img.convert_alpha()
        pacman_buffer = mlx.to_buffer(self.pacman_img)
        pacman.render(pacman_buffer, self.screen_width, game_board,
                      self.window)

        pacman_coords = SpriteCoords(x=0, y=0, w=self.screen_width, h=self.screen_height)
        pacman_sprite = SpriteData(sprite_width=self.screen_width, coords=pacman_coords, buffer=pacman_buffer)

        self.utils.put_sprite_in_image(dest_buffer,
                                       self.screen_height,
                                       0, 0, self.screen_width,
                                       self.screen_height, pacman_sprite)

        del dest_buffer

        mlx.blit_img(dest_img, self.window, (0, 0))
        mlx.update_window()
