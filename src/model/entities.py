import logging
from abc import ABC, abstractmethod
from enum import Enum, auto
from .level_builder import LevelBuilder

logger = logging.getLogger(__name__)


class GhostName(Enum):
    BLINKY = "blinky"
    PINKY = "pinky"
    INKY = "inky"
    CLYDE = "clyde"


class GhostState(Enum):
    NORMAL = auto()
    FRIGHTENED = auto()
    EATEN = auto()


class Entity(ABC):
    def __init__(
            self,
            current_y: int,
            current_x: int,
            current_level: LevelBuilder) -> None:

        self.current_pos_x: int = current_x
        self.current_pos_y: int = current_y
        self.move_x: int = 0
        self.move_y: int = 0
        self.spawn_x: int = current_x
        self.spawn_y: int = current_y
        self.grid: list[list[int]] = current_level.maze.grid
        self.width_max: int = current_level.width
        self.height_max: int = current_level.height
        self.ghost = current_level.ghosts
        self.pacman = current_level.player
        self.speed: float = 1

    def respawn(self) -> None:
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.dir_x = 0
        self.dir_y = 0

    def can_move(self, dir_y: int, dir_x: int) -> bool:

        next_move_y = self.current_pos_y + dir_y
        next_move_x = self.current_pos_x + dir_x
        if 0 < next_move_y >= self.height_max:
            return False
        if 0 < next_move_x >= self.width_max:
            return False

        move_masks: dict[tuple[int, int], int] = {
            (-1, 0): 1,
            (1, 0): 4,
            (0, -1): 8,
            (0, 1): 2,
        }
        mask = move_masks.get((dir_y, dir_x))
        if mask is None:
            return False
        cell_value: int = self.grid[self.current_pos_y][self.current_pos_x]
        return (cell_value & mask) != 0

    @abstractmethod
    def update(self, elapsed_time: float) -> None:
        pass


class PacMan(Entity):
    def __init__(self, y: int, x: int, current_level: LevelBuilder) -> None:
        super().__init__(y, x, current_level)


    def update(self, elapsed_time: float) -> None:
        pass


class Ghost(Entity, ABC):

    def __init__(self, y: int, x: int, current_level: LevelBuilder) -> None:
        super().__init__(y, x, current_level)
        self.state: GhostState = GhostState.NORMAL
        self.respawn_timer: float = 0.0

    def get_eaten(self, respawn_delay: float = 8.0) -> None:
        self.state = GhostState.EATEN
        self.respawn_timer = respawn_delay

    def respawn(self) -> None:
        super().respawn()
        self.state = GhostState.NORMAL

    def update(self, elapsed_time: float) -> None:
        if self.state == GhostState.EATEN:
            self.respawn_timer -= elapsed_time
            if self.respawn_timer <= 0:
                self.respawn()
            return
        if self.state == GhostState.NORMAL:
            self.chase_behavior()
        elif self.state == GhostState.FRIGHTENED:
            self.flee_behavior()

    @abstractmethod
    def chase_behavior(self) -> None:
        pass

    @abstractmethod
    def flee_behavior(self) -> None:
        pass


class Blinky(Ghost):

    def chase_behavior(self) -> None:
        if self.pacman is None:
            return
        target_y, target_x = (
            self.pacman.current_pos_y, self.pacman.current_pos_x)
        possible_directions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]
        for dir_y, dir_x in possible_directions:
            if self.can_move(dir_y, dir_x):
                next_y = dir_y + self.current_pos_y
                next_x = dir_x + self.current_pos_x
            

    def flee_behavior(self) -> None:
        pass


class Pinky(Ghost):
    def chase_behavior(self) -> None:
        pass

    def flee_behavior(self) -> None:
        pass


class Inky(Ghost):
    def chase_behavior(self) -> None:
        pass

    def flee_behavior(self) -> None:
        pass


class Clyde(Ghost):
    def chase_behavior(self) -> None:
        pass

    def flee_behavior(self) -> None:
        pass
