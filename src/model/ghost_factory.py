from .entities import Ghost, Blinky, Pinky, Inky, Clyde, GhostName
from . import level_builder


class GhostFactory:

    @staticmethod
    def create(
            name: GhostName,
            x: int,
            y: int,
            current_level: "level_builder.LevelBuilder") -> Ghost:

        match name:
            case GhostName.BLINKY:
                return Blinky(y, x, current_level)
            case GhostName.PINKY:
                return Pinky(y, x, current_level)
            case GhostName.INKY:
                return Inky(y, x, current_level)
            case GhostName.CLYDE:
                return Clyde(y, x, current_level)
