from dataclasses import dataclass
from .maze_adaptater import MazeAdapter
from .entities import PacMan, Ghost
from ..shared import GhostName, Vector2D


@dataclass
class GameBoard:
    """Collect maze, entities, and collectible positions for a level."""

    maze: MazeAdapter
    player: PacMan
    player_spawn_pos: Vector2D
    ghosts: dict[GhostName, Ghost]
    ghosts_spawn_pos: dict[GhostName, Vector2D]
    pacgums: int
    pacgum_pos: set[Vector2D]
    super_pacgums_pos: set[Vector2D]

    def reset_entities(self) -> None:
        """Respawn the player and all ghosts at their starting positions."""
        self.player.respawn()
        for ghost in self.ghosts.values():
            ghost.respawn()
