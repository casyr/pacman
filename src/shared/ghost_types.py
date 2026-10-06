from enum import Enum, auto


class GhostName(Enum):
    BLINKY = "blinky"
    PINKY = "pinky"
    INKY = "inky"
    CLYDE = "clyde"


class GhostState(Enum):
    NORMAL = auto()
    FRIGHTENED = auto()
    FRIGHTENED_END = auto()
    EATEN = auto()
