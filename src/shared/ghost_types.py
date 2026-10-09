from enum import Enum, auto


class GhostName(Enum):
    """Names of the four ghosts in the game."""

    BLINKY = "blinky"
    PINKY = "pinky"
    INKY = "inky"
    CLYDE = "clyde"


class GhostState(Enum):
    """Possible behavioral states for a ghost."""

    NORMAL = auto()
    FRIGHTENED = auto()
    FRIGHTENED_END = auto()
    EATEN = auto()
