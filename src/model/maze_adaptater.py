import logging
from mazegenerator import MazeGenerator
from ..errors import MazeError

logger = logging.getLogger(__name__)


class MazeAdapter:

    def __init__(self, width: int, height: int, seed: int) -> None:
        self.width = width
        self.height = height
        self.seed = seed
        self.grid: list[list[int]] = []

    def generate_level(self) -> None:
        try:
            generate_maze = MazeGenerator(
                size=(self.width, self.height),
                perfect=False,
                seed=self.seed
            )
            self.grid = generate_maze.maze
        except Exception as error:
            raise MazeError(f"Maze generator module error: {error}")
