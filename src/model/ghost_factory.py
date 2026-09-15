from .entities import Ghost, Blinky, Pinky, Inky, Clyde, GhostName
from .level_builder import LevelBuilder


class GhostFactory:

    @staticmethod
    def create(
            name: GhostName,
            x: int,
            y: int,
            current_level: LevelBuilder) -> Ghost:

        factories = {
            GhostName.BLINKY: Blinky,
            GhostName.PINKY: Pinky,
            GhostName.INKY: Inky,
            GhostName.CLYDE: Clyde,
        }

        ghost_class = factories.get(name)
        return ghost_class(y, x, current_level)
