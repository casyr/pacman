import logging
from abc import ABC, abstractmethod
from .maze_adaptater import MazeAdapter
from ..shared import GhostName, Vector2D, Direction, GhostState, Wall

logger = logging.getLogger(__name__)


class Entity(ABC):
    def __init__(
            self,
            current_y: int,
            current_x: int,
            maze: MazeAdapter) -> None:

        self.current_pos_y: int = current_y
        self.current_pos_x: int = current_x
        self.move_pixel_y: float = float(current_y)
        self.move_pixel_x: float = float(current_x)
        self.move_dir: Vector2D = Direction.ZERO.value
        self.spawn_pos: Vector2D = Vector2D(current_y, current_x)
        self.previous_pos: Vector2D = Vector2D(current_y, current_x)
        self.grid: list[list[int]] = maze.grid
        self.width_max: int = maze.width
        self.height_max: int = maze.height
        self.speed: float = 1
        self.move_timer: float = 0.0

    def respawn(self) -> None:
        self.current_pos_y = self.spawn_pos.y
        self.current_pos_x = self.spawn_pos.x
        self.move_pixel_y = float(self.spawn_pos.y)
        self.move_pixel_x = float(self.spawn_pos.x)
        self.move_dir = Direction.ZERO.value
        self.previous_pos = self.spawn_pos

    def can_move(self, direction: Vector2D) -> bool:

        move_masks: dict[Vector2D, int] = {
            Direction.NORTH.value: Wall.NORTH.value,
            Direction.SOUTH.value: Wall.SOUTH.value,
            Direction.WEST.value: Wall.WEST.value,
            Direction.EAST.value: Wall.EAST.value,
        }

        mask = move_masks.get(direction)
        if mask is None:
            return False
        cell_value: int = self.grid[self.current_pos_y][self.current_pos_x]
        return not (cell_value & mask)

    def move_continuously(self, elapsed_time: float) -> None:
        if (self.move_dir == Direction.ZERO.value
                or not self.can_move(self.move_dir)):
            self.move_pixel_y = float(self.current_pos_y)
            self.move_pixel_x = float(self.current_pos_x)
            return

        self.move_pixel_y += self.move_dir.y * self.speed * elapsed_time
        self.move_pixel_x += self.move_dir.x * self.speed * elapsed_time

        if abs(self.move_pixel_y - self.current_pos_y) >= 1:
            self.previous_pos = Vector2D(
                self.current_pos_y, self.current_pos_x)
            self.current_pos_y += self.move_dir.y
            self.move_pixel_y = float(self.current_pos_y)
        elif abs(self.move_pixel_x - self.current_pos_x) >= 1:
            self.previous_pos = Vector2D(
                self.current_pos_y, self.current_pos_x)
            self.current_pos_x += self.move_dir.x
            self.move_pixel_x = float(self.current_pos_x)

    @abstractmethod
    def update(self, elapsed_time: float) -> None:
        pass


class PacMan(Entity):

    def __init__(
            self,
            y: int,
            x: int,
            maze: MazeAdapter) -> None:
        super().__init__(y, x, maze)
        self.speed = 2
        self.desired_dir: Vector2D = Direction.ZERO.value
        self.is_dying: bool = False
        self.death_elapsed: float = 0.0
        self.death_duration: float = 1.6

    def start_death_animation(self) -> None:
        self.is_dying = True
        self.death_elapsed = 0.0
        self.move_dir = Direction.ZERO.value

    def death_animation_finished(self) -> bool:
        return self.death_elapsed >= self.death_duration

    def set_direction(self, dir_y: int, dir_x: int) -> None:
        self.desired_dir = Vector2D(dir_y, dir_x)

    def update(self, elapsed_time: float) -> None:
        if self.is_dying:
            self.death_elapsed += elapsed_time
            return

        is_reverse = (
            self.desired_dir.y == -self.move_dir.y
            and self.desired_dir.x == -self.move_dir.x
        )
        if is_reverse and self.can_move(self.desired_dir):
            self.move_dir = self.desired_dir

        is_near_center = (
            abs(self.move_pixel_y - self.current_pos_y) < 0.1
            and abs(self.move_pixel_x - self.current_pos_x) < 0.1
        )
        if is_near_center and self.desired_dir != self.move_dir:
            if self.can_move(self.desired_dir):
                self.move_dir = self.desired_dir
                self.move_pixel_y = float(self.current_pos_y)
                self.move_pixel_x = float(self.current_pos_x)
        self.move_continuously(elapsed_time)
        # self.move_timer += elapsed_time
        # move_delay: float = 1.0 / self.speed
        # if self.move_timer >= move_delay:
        #     self.move_timer -= move_delay
        #     if not self.can_move(self.move_dir):
        #         self.previous_pos = Vector2D(
        #             self.current_pos_y, self.current_pos_x)
        #         self.move_dir = Direction.ZERO.value
        #         return

        #     self.previous_pos = Vector2D(
        #         self.current_pos_y, self.current_pos_x)
        #     self.current_pos_y += self.move_dir.y
        #     self.current_pos_x += self.move_dir.x


class Ghost(Entity, ABC):

    def __init__(
            self,
            y: int,
            x: int,
            maze: MazeAdapter,
            pacman: PacMan,
            ghosts: list['Ghost'],
            name: GhostName,
            ) -> None:
        super().__init__(y, x, maze)
        self.name: GhostName = name
        self.pacman: PacMan = pacman
        self.ghosts: list[Ghost] = ghosts
        self.state: GhostState = GhostState.NORMAL
        self.respawn_timer: float = 0.0

    def get_eaten(self, respawn_delay: float = 1.0) -> None:
        self.state = GhostState.EATEN
        self.respawn_timer = respawn_delay

    def respawn(self) -> None:
        super().respawn()
        self.state = GhostState.NORMAL
        self.respawn_timer = 0.0

    def update(self, elapsed_time: float) -> None:
        if self.state == GhostState.EATEN:
            self.respawn_timer -= elapsed_time
            if self.respawn_timer <= 0:
                self.respawn()
            return
        is_centered = (
            abs(self.move_pixel_y - self.current_pos_y) < 0.001
            and abs(self.move_pixel_x - self.current_pos_x) < 0.001
        )
        current_tile = Vector2D(self.current_pos_y, self.current_pos_x)
        if is_centered:
            self.move_pixel_y = float(self.current_pos_y)
            self.move_pixel_x = float(self.current_pos_x)
            self.decision_made_on_tile = current_tile
            if self.state == GhostState.NORMAL:
                target = self.get_target()
                if target is not None:
                    self.chase_behavior(target)
            elif self.state == GhostState.FRIGHTENED:
                self.flee_behavior()
        self.move_continuously(elapsed_time)
        # self.move_timer += elapsed_time
        # move_delay: float = 1.0 / self.speed
        # if self.move_timer >= move_delay:
        #     self.move_timer -= move_delay

        #     if self.state == GhostState.NORMAL:
        #         target = self.get_target()
        #         if target is not None:
        #             self.chase_behavior(target)
        #     elif self.state == GhostState.FRIGHTENED:
        #         self.flee_behavior()

    @abstractmethod
    def get_target(self) -> Vector2D:
        pass

    def chase_behavior(self, target: Vector2D) -> None:
        possible_directions: list[Vector2D] = [
            Direction.NORTH.value, Direction.WEST.value,
            Direction.SOUTH.value, Direction.EAST.value
        ]
        best_direction: Vector2D = Direction.ZERO.value
        valid_choice: bool = False
        min_distance = float('inf')
        dist = float('inf')

        for direction in possible_directions:
            if not self.can_move(direction):
                continue
            next_pos = Vector2D(
                self.current_pos_y + direction.y,
                self.current_pos_x + direction.x
            )

            if next_pos != self.previous_pos:
                valid_choice = True
                dist = (
                    (next_pos.y - target.y) ** 2 + (next_pos.x - target.x) ** 2
                    )
                if dist < min_distance:
                    min_distance = dist
                    best_direction = direction

        if not valid_choice:
            best_direction = Vector2D(
                self.previous_pos.y - self.current_pos_y,
                self.previous_pos.x - self.current_pos_x
            )
        self.move_dir = best_direction

    def flee_behavior(self) -> None:
        possible_directions: list[Vector2D] = [
            Direction.NORTH.value, Direction.WEST.value,
            Direction.SOUTH.value, Direction.EAST.value
        ]
        best_direction: Vector2D = Direction.ZERO.value
        valid_choice: bool = False
        max_distance = float('-inf')
        dist = float('-inf')

        target = Vector2D(self.pacman.current_pos_y, self.pacman.current_pos_x)

        for direction in possible_directions:
            if not self.can_move(direction):
                continue

            next_pos = Vector2D(
                self.current_pos_y + direction.y,
                self.current_pos_x + direction.x
            )

            if next_pos != self.previous_pos:
                valid_choice = True
                dist = (
                    (next_pos.y - target.y) ** 2 + (next_pos.x - target.x) ** 2
                    )
                if dist >= max_distance:
                    max_distance = dist
                    best_direction = direction

        if not valid_choice:
            best_direction = Vector2D(
                self.previous_pos.y - self.current_pos_y,
                self.previous_pos.x - self.current_pos_x
            )

        self.move_dir = best_direction


class Blinky(Ghost):

    def get_target(self) -> Vector2D:
        return Vector2D(self.pacman.current_pos_y, self.pacman.current_pos_x)


class Pinky(Ghost):

    def get_target(self) -> Vector2D:
        target_y = self.pacman.current_pos_y + (self.pacman.move_dir.y * 4)
        target_x = self.pacman.current_pos_x + (self.pacman.move_dir.x * 4)
        return Vector2D(target_y, target_x)


class Inky(Ghost):
    def _get_blinky(self) -> Ghost | None:
        for ghost in self.ghosts:
            if isinstance(ghost, Blinky):
                return ghost
        return None

    def get_target(self) -> Vector2D:
        blinky = self._get_blinky()
        if blinky is None:
            return self.spawn_pos

        front_y = self.pacman.current_pos_y + (self.pacman.move_dir.y * 2)
        front_x = self.pacman.current_pos_x + (self.pacman.move_dir.x * 2)
        target_y = front_y + (front_y - blinky.current_pos_y)
        target_x = front_x + (front_x - blinky.current_pos_x)
        return Vector2D(target_y, target_x)


class Clyde(Ghost):
    def get_target(self) -> Vector2D:
        dist_case = (
            abs(self.current_pos_y - self.pacman.current_pos_y) +
            abs(self.current_pos_x - self.pacman.current_pos_x)
        )
        if dist_case < 8:
            return self.spawn_pos
        else:
            return Vector2D(
                self.pacman.current_pos_y, self.pacman.current_pos_x)
