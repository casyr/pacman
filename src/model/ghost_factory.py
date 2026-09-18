from .entities import Ghost, Blinky, Pinky, Inky, Clyde, GhostName
from .maze_adaptater import MazeAdapter
from .entities import PacMan


class GhostFactory:

    @staticmethod
    def create(
            name: GhostName,
            pos_y: int,
            pos_x: int,
            maze: MazeAdapter,
            pacman: PacMan,
            ghosts: list[Ghost]) -> Ghost:

        match name:
            case GhostName.BLINKY:
                return Blinky(pos_y, pos_x, maze, pacman, ghosts)
            case GhostName.PINKY:
                return Pinky(pos_y, pos_x, maze, pacman, ghosts)
            case GhostName.INKY:
                return Inky(pos_y, pos_x, maze, pacman, ghosts)
            case GhostName.CLYDE:
                return Clyde(pos_y, pos_x, maze, pacman, ghosts)
            case _:
                raise ValueError(f"Unknown ghost type: {name}")
