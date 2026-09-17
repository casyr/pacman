from dataclasses import dataclass
from .maze_adaptater import MazeAdapter
from .entities import PacMan, Ghost, GhostName


@dataclass
class GameBoard:
    maze: MazeAdapter
    player: PacMan
    player_spawn_pos: tuple[int, int]
    ghosts: list[Ghost]
    ghosts_spawn_pos: dict[GhostName, tuple[int, int]]
    pacgums: int
    pacgum_pos: set[tuple[int, int]]
    super_pacgums_pos: set[tuple[int, int]]
