import logging
from abc import ABC, abstractmethod
from enum import Enum, auto
from . import level_builder

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
            current_level: "level_builder.LevelBuilder") -> None:

        self.current_pos_x: int = current_x
        self.current_pos_y: int = current_y
        self.move_x: int = 0
        self.move_y: int = 0
        self.spawn_x: int = current_x
        self.spawn_y: int = current_y
        self.previous_pos: tuple[int, int] = (current_y, current_x)
        self.grid: list[list[int]] = current_level.maze.grid
        self.width_max: int = current_level.width
        self.height_max: int = current_level.height
        self.ghost = current_level.ghosts
        self.pacman = current_level.player
        self.speed: float = 1

    def respawn(self) -> None:
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.move_x = 0
        self.move_y = 0

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

    def __init__(
            self,
            y: int,
            x: int,
            current_level: "level_builder.LevelBuilder") -> None:
        super().__init__(y, x, current_level)

    def update(self, elapsed_time: float) -> None:
        pass


class Ghost(Entity, ABC):

    def __init__(
            self,
            y: int,
            x: int,
            current_level: "level_builder.LevelBuilder") -> None:
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
            target = self.get_target()
            if target is not None:
                self.chase_behavior(target[0], target[1])
        elif self.state == GhostState.FRIGHTENED:
            self.flee_behavior()

    @abstractmethod
    def get_target(self) -> tuple[int, int]:
        pass

    def chase_behavior(self, target_y: int, target_x: int) -> None:
        possible_directions: list[tuple[int, int]] = [
            (-1, 0), (0, -1), (1, 0), (0, 1)]
        best_direction: tuple[int, int] = (0, 0)
        valid_choice: bool = False
        min_distance = float('inf')
        dist = float('inf')

        for dir_y, dir_x in possible_directions:
            if not self.can_move(dir_y, dir_x):
                continue
            next_y: int = dir_y + self.current_pos_y
            next_x: int = dir_x + self.current_pos_x

            if (next_y, next_x) != self.previous_pos:
                valid_choice = True
                dist = (next_y - target_y) ** 2 + (next_x - target_x) ** 2
                if dist < min_distance:
                    min_distance = dist
                    best_direction = (dir_y, dir_x)

        if not valid_choice:
            best_direction = (
                (self.previous_pos[0] - self.current_pos_y),
                (self.previous_pos[1] - self.current_pos_x)
            )

        self.previous_pos = (self.current_pos_y, self.current_pos_x)
        self.current_pos_y += best_direction[0]
        self.current_pos_x += best_direction[1]

    def flee_behavior(self) -> None:
        possible_directions: list[tuple[int, int]] = [
            (-1, 0), (0, -1), (1, 0), (0, 1)]
        best_direction: tuple[int, int] = (0, 0)
        valid_choice: bool = False
        max_distance = float('-inf')
        dist = float('-inf')

        if self.pacman is None:
            return

        target_y, target_x = (
            self.pacman.current_pos_y, self.pacman.current_pos_x)

        for dir_y, dir_x in possible_directions:
            if not self.can_move(dir_y, dir_x):
                continue
            next_y: int = dir_y + self.current_pos_y
            next_x: int = dir_x + self.current_pos_x

            if (next_y, next_x) != self.previous_pos:
                valid_choice = True
                dist = (next_y - target_y) ** 2 + (next_x - target_x) ** 2
                if dist >= max_distance:
                    max_distance = dist
                    best_direction = (dir_y, dir_x)

        if not valid_choice:
            best_direction = (
                (self.previous_pos[0] - self.current_pos_x),
                (self.previous_pos[1] - self.current_pos_y)
            )

        self.previous_pos = (self.current_pos_y, self.current_pos_x)
        self.current_pos_y += best_direction[0]
        self.current_pos_x += best_direction[1]


class Blinky(Ghost):

    def get_target(self) -> tuple[int, int]:
        if self.pacman is None:
            return (0, 0)
        return (self.pacman.current_pos_y, self.pacman.current_pos_x)


class Pinky(Ghost):

    def get_target(self) -> tuple[int, int]:
        if self.pacman is None:
            return (0, 0)
        target_y = self.pacman.current_pos_y + (self.pacman.move_y * 4)
        target_x = self.pacman.current_pos_x + (self.pacman.move_x * 4)

        return (target_y, target_x)


class Inky(Ghost):
    def _get_blinky(self) -> Ghost | None:
        return self.ghost[2]

    def get_target(self) -> tuple[int, int]:
        if self.pacman is None:
            return (0, 0)
        blinky = self._get_blinky()
        if blinky is None:
            return (self.spawn_y, self.spawn_x)

        front_y = self.pacman.current_pos_y + (self.pacman.move_y * 2)
        front_x = self.pacman.current_pos_x + (self.pacman.move_x * 2)
        target_y = front_y + (front_y - blinky.current_pos_y)
        target_x = front_x + (front_x - blinky.current_pos_x)
        return (target_y, target_x)


class Clyde(Ghost):
    def get_target(self) -> tuple[int, int]:
        if self.pacman is None:
            return (0, 0)
        dist_case = (
            abs(self.current_pos_y - self.pacman.current_pos_y) +
            abs(self.current_pos_x - self.pacman.current_pos_x)
        )
        if dist_case < 8:
            return (self.spawn_y, self.spawn_x)
        else:
            return (self.pacman.current_pos_y, self.pacman.current_pos_x)
