from pygame import Surface
from . import mlx_wrapper as mlx
from .maze_creator import MazeView
from .pacgum import PacgumsView
from .entities_view import GhostView, PacmanView
from .displayer_utils import DisplayerUtils
from .menu import BaseMenuView
from .session_view import SessionView
from ..model import GameBoard, GameSession
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from ..errors import ViewError


class PlayingView(BaseMenuView):
    """Compose and render the active gameplay layers."""

    def __init__(self, screen_width: int, screen_height: int,
                 window: Surface, sprite_sheet: SpriteSheetsManager):
        """Create the view's image layers and rendering state.

        Args:
            screen_width: Display width in pixels.
            screen_height: Display height in pixels.
            window: Surface used to display the game.
            sprite_sheet: Sprite assets used by gameplay views.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window = window
        self.sprite_sheets = sprite_sheet
        self.game_board: GameBoard | None = None
        self.maze: MazeView | None = None
        self.pacgums: PacgumsView | None = None
        self.pacman: PacmanView | None = None
        self.session_info: SessionView | None = None
        self.ghostView = GhostView | None

        self.maze_img = mlx.new_image(
            self.screen_width, self.screen_height)

        self.dynamic_img = mlx.new_image(
            self.screen_width, self.screen_height).convert_alpha()

        self.utils = DisplayerUtils()

    def load_level(self, game_board: GameBoard) -> None:
        """Create renderers and static layers for a game board.

        Args:
            game_board: Board whose level should be loaded.
        """
        self.game_board = game_board
        self.maze = MazeView(game_board,
                             self.sprite_sheets,
                             self.screen_width,
                             self.screen_height)

        self.pacgums = PacgumsView(game_board,
                                   self.sprite_sheets,
                                   self.screen_width,
                                   self.screen_height)

        self.pacman = PacmanView(game_board,
                                 self.sprite_sheets,
                                 self.screen_width,
                                 self.screen_height)

        self.session_info = SessionView(self.screen_width,
                                        self.screen_height,
                                        self.window,
                                        self.sprite_sheets)

        self.ghosts = GhostView(game_board,
                                self.sprite_sheets,
                                self.screen_width,
                                self.screen_height)

        self._build_maze()

    def _build_maze(self) -> None:
        """Build the static maze layer and place its pacgums."""
        if (
            self.maze is None
            or self.game_board is None
            or self.pacgums is None
        ):
            return

        mlx.clear_window(self.maze_img)
        maze_buf = mlx.to_buffer(self.maze_img)
        self.maze.render(
            maze_buf, self.screen_width, self.game_board, self.window)
        self.pacgums.render(maze_buf, self.screen_width)
        del maze_buf

    def erase_pacgum(self, grid_y: int, grid_x: int) -> None:
        """Erase a collected pacgum from the cached maze image.

        Args:
            grid_y: Pacgum row in the maze grid.
            grid_x: Pacgum column in the maze grid.
        """
        if self.pacman is None:
            return
        tile_size = self.pacman.tile_size
        y_start = self.pacman.y_start
        x_start = self.pacman.x_start

        pos_y = y_start + grid_y * tile_size
        pos_x = x_start + grid_x * tile_size
        gum_size = max(4, tile_size // 3)
        offset = (tile_size - gum_size) // 2
        erase_y = pos_y + offset
        erase_x = pos_x + offset
        buffer = mlx.to_buffer(self.maze_img, False)
        sprite = self.sprite_sheets.sprites.get("empty_tile")
        if sprite is None:
            raise ViewError("maze_sprites.yaml is missing or invalid")
        self.utils.put_sprite_in_image(
            buffer,
            self.screen_width,
            erase_x,
            erase_y,
            gum_size,
            gum_size,
            self.sprite_sheets.sprites.get("empty_" "tile"),
        )
        del buffer

    def clear_all_layers(self) -> None:
        """Clear cached layers, the display, and refresh the window."""
        mlx.clear_window(self.maze_img)
        mlx.clear_window(self.dynamic_img)
        mlx.clear_window(self.window)
        mlx.update_window()

    def render(self, game_board: GameBoard,
               game_session: GameSession) -> None:
        """Draw the dynamic game state over the cached maze.

        Args:
            game_board: Board containing current entity positions.
            game_session: Session state shown in the HUD.
        """
        self.dynamic_img.blit(self.maze_img, (0, 0))

        if self.pacman is None:
            return

        dynamic_buffer = mlx.to_buffer(self.dynamic_img, False)
        try:
            self.pacman.render(dynamic_buffer,
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
        except KeyError:
            raise ViewError("problem found in a .yaml file"
                            " (file is invalid or is missing)")

        mlx.blit_img(self.dynamic_img, self.window, (0, 0))
        mlx.update_window()
