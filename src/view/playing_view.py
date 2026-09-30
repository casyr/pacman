from .maze import Maze
from .pacgums import Pacgums
from . import mlx_wrapper as mlx
from ..controller import GameContext


class PlayingView():

    def __init__(self, context: GameContext):
        self.context = context
        self.maze_image = mlx.new_image(context.screen_width,
                                        context.screen_height).convert_alpha()
        self.maze_buffer = mlx.to_buffer(self.maze_image)

    def render(self, is_updated: bool) -> None:

        if is_updated:
            maze = Maze(self.context.game_board,
                        self.context.sprite_sheets,
                        self.context.window)
            dest_width = self.context.window.get_width()

            mlx.clear_window(self.context.window)
            maze.render(self.maze_buffer, dest_width)

        pacgum = Pacgums(self.context.game_board,
                         self.context.sprite_sheets,
                         self.context.window)

        pacgum_image = mlx.new_image(self.context.screen_width,
                                     self.context.screen_height
                                     ).convert_alpha()
        pacgum_buffer = mlx.to_buffer(pacgum_image)
        pacgum.render(pacgum_buffer, self.context.screen_width)
        del self.maze_buffer
        del pacgum_buffer
        mlx.blit_img(self.maze_image, self.context.window, (0, 0))
        mlx.blit_img(pacgum_image, self.context.window, (0, 0))
        mlx.update_window()
