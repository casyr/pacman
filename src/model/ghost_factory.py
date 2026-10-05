from .entities import Ghost, Blinky, Pinky, Inky, Clyde
from .maze_adaptater import MazeAdapter
from .entities import PacMan
from ..shared import GhostName, Vector2D


class GhostFactory:

    @staticmethod
    def create(
            name: GhostName,
            pos: Vector2D,
            maze: MazeAdapter,
            pacman: PacMan,
            ghosts: dict[GhostName, Ghost]) -> Ghost:

        match name:
            case GhostName.BLINKY:
                return Blinky(pos.y, pos.x, maze, pacman, ghosts, name)
            case GhostName.PINKY:
                return Pinky(pos.y, pos.x, maze, pacman, ghosts, name)
            case GhostName.INKY:
                return Inky(pos.y, pos.x, maze, pacman, ghosts, name)
            case GhostName.CLYDE:
                return Clyde(pos.y, pos.x, maze, pacman, ghosts, name)
            case _:
                raise ValueError(f"Unknown ghost type: {name}")
