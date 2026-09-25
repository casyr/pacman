from dataclasses import dataclass
from .maze_adaptater import MazeAdapter
from .entities import PacMan, Ghost
from ..shared import GhostName, Vector2D


@dataclass
class GameBoard:
    maze: MazeAdapter
    player: PacMan
    player_spawn_pos: Vector2D
    ghosts: list[Ghost]
    ghosts_spawn_pos: dict[GhostName, Vector2D]
    pacgums: int
    pacgums_pos: set[Vector2D]
    super_pacgums_pos: set[Vector2D]
