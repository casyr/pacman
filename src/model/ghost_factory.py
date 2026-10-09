from .entities import Ghost, Blinky, Pinky, Inky, Clyde
from .maze_adaptater import MazeAdapter
from .entities import PacMan
from ..shared import GhostName, Vector2D


class GhostFactory:
    """Construct ghost instances for the requested ghost type."""

    @staticmethod
    def create(
            name: GhostName,
            pos: Vector2D,
            maze: MazeAdapter,
            pacman: PacMan) -> Ghost:
        """Create a ghost at a position and bind it to the maze and player.

        Args:
            name: Type of ghost to create.
            pos: Initial row and column.
            maze: Maze the ghost moves through.
            pacman: Player character the ghost tracks.

        Returns:
            A ghost instance matching the requested type.
        """

        match name:
            case GhostName.BLINKY:
                return Blinky(pos.y, pos.x, maze, pacman)
            case GhostName.PINKY:
                return Pinky(pos.y, pos.x, maze, pacman)
            case GhostName.INKY:
                return Inky(pos.y, pos.x, maze, pacman)
            case GhostName.CLYDE:
                return Clyde(pos.y, pos.x, maze, pacman)
            case _:
                raise ValueError(f"Unknown ghost type: {name}")
