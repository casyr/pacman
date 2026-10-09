import logging
from mazegenerator import MazeGenerator
from ..errors import MazeError

logger = logging.getLogger(__name__)


class MazeAdapter:
    """Generate and expose a maze grid for a level."""

    def __init__(self, width: int, height: int, seed: int) -> None:
        """Initialize maze dimensions, seed, and an empty grid.

        Args:
            width: Number of columns in the maze.
            height: Number of rows in the maze.
            seed: Seed used for deterministic generation.
        """
        self.width = width
        self.height = height
        self.seed = seed
        self.grid: list[list[int]] = []

    def generate_level(self) -> None:
        """Generate the maze grid or raise a maze-specific error."""
        try:
            generate_maze = MazeGenerator(
                size=(self.width, self.height),
                perfect=False,
                seed=self.seed
            )
            self.grid = generate_maze.maze
        except Exception as error:
            raise MazeError(f"Maze generator module error: {error}")
