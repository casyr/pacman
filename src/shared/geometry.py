from enum import Enum
from typing import NamedTuple


class Vector2D(NamedTuple):
    y: int
    x: int


class Direction(Enum):
    NORTH = Vector2D(-1, 0)
    EAST = Vector2D(0, 1)
    SOUTH = Vector2D(1, 0)
    WEST = Vector2D(0, -1)
    ZERO = Vector2D(0, 0)


class Wall(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


class GridBounds(NamedTuple):
    width: int
    height: int

    @property
    def corners(self) -> list[Vector2D]:
        """Retourne les 4 coins de la grille en fonction de sa taille."""
        return [
            Vector2D(0, 0),
            Vector2D(0, self.width - 1),
            Vector2D(self.height - 1, 0),
            Vector2D(self.height - 1, self.width - 1),
        ]
