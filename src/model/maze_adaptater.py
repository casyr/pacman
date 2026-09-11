from mazegenerator import MazeGenerator
from ..errors import MazeError


class MazeAdapter:

    def __init__(self, width: int, height: int, seed: int) -> None:
        self.width = width
        self.height = height
        self.seed = seed

    def generate_level(self) -> list[list[int]]:
        try:
            generator = MazeGenerator(
                size=(self.width, self.height),
                perfect=False,
                seed=self.seed
            )
            grid: list[list[int]] = generator.maze
            return grid
        except Exception as error:
            raise MazeError(f"Maze generator module error: {error}")
