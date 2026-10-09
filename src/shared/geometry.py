from enum import Enum
from typing import NamedTuple


class Vector2D(NamedTuple):
    """Grid coordinate with vertical and horizontal components."""

    y: int
    x: int


class Direction(Enum):
    """Cardinal directions and the zero movement vector."""

    NORTH = Vector2D(-1, 0)
    EAST = Vector2D(0, 1)
    SOUTH = Vector2D(1, 0)
    WEST = Vector2D(0, -1)
    ZERO = Vector2D(0, 0)


class Wall(Enum):
    """Bit flags identifying the four walls of a grid cell."""

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8


class GridBounds(NamedTuple):
    """Width and height of a rectangular grid."""

    width: int
    height: int

    @property
    def corners_pos(self) -> list[Vector2D]:
        """Return the four corner coordinates of the grid.

        Returns:
            Coordinates ordered from top-left clockwise.
        """
        return [
            Vector2D(0, 0),
            Vector2D(0, self.width - 1),
            Vector2D(self.height - 1, 0),
            Vector2D(self.height - 1, self.width - 1),
        ]
