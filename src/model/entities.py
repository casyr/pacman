import logging
import heapq
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
        self.move_dir_state: Direction = Direction.ZERO
        self.spawn_pos: Vector2D = Vector2D(current_y, current_x)
        self.previous_pos: Vector2D = Vector2D(current_y, current_x)
        self.grid: list[list[int]] = maze.grid
        self.width_max: int = maze.width
        self.height_max: int = maze.height
        self.speed: float = 1.5
        self.move_timer: float = 0.0
        self.center_tolerance: float = 0.05

    def respawn(self) -> None:
        self.current_pos_y = int(self.spawn_pos.y)
        self.current_pos_x = int(self.spawn_pos.x)
        self.move_pixel_y = float(self.spawn_pos.y)
        self.move_pixel_x = float(self.spawn_pos.x)
        self.move_dir = Direction.ZERO.value
        self.previous_pos = self.spawn_pos
        self.is_dying: bool = False

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

        cell_value: int = (self.grid[int(self.current_pos_y)]
                           [int(self.current_pos_x)])
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
            self.current_pos_y += int(self.move_dir.y)
            self.move_pixel_y = float(self.current_pos_y)
        elif abs(self.move_pixel_x - self.current_pos_x) >= 1:
            self.previous_pos = Vector2D(
                self.current_pos_y, self.current_pos_x)
            self.current_pos_x += int(self.move_dir.x)
            self.move_pixel_x = float(self.current_pos_x)

    def is_moving(self) -> bool:
        if self.move_dir == Direction.ZERO.value:
            return False
        return self.can_move(self.move_dir)

    def is_at_intersection(self) -> bool:
        return (
            abs(self.move_pixel_y - self.current_pos_y) < self.center_tolerance
            and abs(
                self.move_pixel_x - self.current_pos_x) < self.center_tolerance
        )

    def perfectly_aligns(self) -> None:
        self.move_pixel_y = float(self.current_pos_y)
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
        self.desired_state_dir = Direction.ZERO
        self.is_dying: bool = False
        self.death_elapsed: float = 0.0
        self.death_duration: float = 1.6
        self.animation_timer: float = 0.0

    def start_death_animation(self) -> None:
        self.is_dying = True
        self.death_elapsed = 0.0
        self.move_dir = Direction.ZERO.value

    def death_animation_finished(self) -> bool:
        return self.death_elapsed >= self.death_duration

    def set_direction(self, direction: Direction) -> None:
        self.desired_dir = direction.value
        self.desired_state_dir = direction

    def is_reversing(self) -> bool:
        return (
            self.desired_dir.y == -self.move_dir.y
            and self.desired_dir.x == -self.move_dir.x
        )

    def handle_death_animation(self, elapsed_time: float) -> None:
        self.death_elapsed += elapsed_time
        self.animation_timer = 0.0

    def update(self, elapsed_time: float) -> None:

        if self.is_dying:
            self.handle_death_animation(elapsed_time)
            return

        if self.is_moving():
            self.death_elapsed = 0.0
            self.animation_timer += elapsed_time

        if self.is_reversing() and self.can_move(self.desired_dir):
            self.move_dir = self.desired_dir
            self.move_dir_state = self.desired_state_dir

        if self.is_at_intersection() and self.desired_dir != self.move_dir:
            if self.can_move(self.desired_dir):
                self.move_dir = self.desired_dir
                self.move_dir_state = self.desired_state_dir
                self.perfectly_aligns()

        self.move_continuously(elapsed_time)


class Ghost(Entity, ABC):

    def __init__(
            self,
            y: int,
            x: int,
            maze: MazeAdapter,
            pacman: PacMan,
            ghosts: dict[GhostName, 'Ghost'],
            name: GhostName,
            ) -> None:
        super().__init__(y, x, maze)
        self.name: GhostName = name
        self.pacman: PacMan = pacman
        self.ghosts: dict[GhostName, Ghost] = ghosts
        self.state: GhostState = GhostState.NORMAL
        self.respawn_timer: float = 0.0
        self.decision_made_on_tile: Vector2D | None = None
        self.animation_timer: float = 0.0
        self.possible_directions: list[Direction] = [
            Direction.NORTH, Direction.WEST,
            Direction.SOUTH, Direction.EAST
        ]
        self.wall_check = {
                Direction.NORTH: Wall.NORTH.value,
                Direction.EAST: Wall.EAST.value,
                Direction.SOUTH: Wall.SOUTH.value,
                Direction.WEST: Wall.WEST.value
            }

    def get_eaten(self, respawn_delay: float = 1.0) -> None:
        self.state = GhostState.EATEN
        self.respawn_timer = respawn_delay

    def respawn(self) -> None:
        super().respawn()
        self.state = GhostState.NORMAL
        self.respawn_timer = 0.0
        self.decision_made_on_tile = None

    def update(self, elapsed_time: float) -> None:
        if self.state == GhostState.EATEN:
            self.respawn_timer -= elapsed_time
            if self.respawn_timer <= 0:
                self.respawn()
            return
        self.animation_timer += elapsed_time
        current_tile = Vector2D(self.current_pos_y, self.current_pos_x)
        if (self.is_at_intersection()
                and self.decision_made_on_tile != current_tile):
            self.decision_made_on_tile = current_tile

            if self.state == GhostState.NORMAL:
                target = self.get_target()
                if target is not None:
                    self.chase_behavior(
                        self.current_pos_y,
                        self.current_pos_x,
                        target)
            elif (self.state == GhostState.FRIGHTENED or
                  self.state == GhostState.FRIGHTENED_END):
                self.flee_behavior()
        self.move_continuously(elapsed_time)

    @abstractmethod
    def get_target(self) -> Vector2D:
        pass

    def chase_behavior(
            self,
            current_pos_y: int,
            current_pos_x: int,
            target: Vector2D) -> None:

        start: Vector2D = Vector2D(current_pos_y, current_pos_x)
        distances: dict[Vector2D, int] = {start: 0}
        came_from: dict[Vector2D, Vector2D | None] = {start: None}
        queue: list[tuple[int, Vector2D]] = [(0, start)]
        if (target.x >= self.width_max or target.y >= self.height_max or
                target.x <= 0 or target.y <= 0):
            target = Vector2D(
                self.pacman.current_pos_y, self.pacman.current_pos_x)

        while queue:
            current_cost, current_pos = heapq.heappop(queue)
            if current_pos == target:
                return self.get_path(came_from, target)
            if current_cost > distances.get(
                    current_pos, float('inf')):
                continue
            for direction in self.possible_directions:
                if (self.grid[int(current_pos.y)][int(current_pos.x)] &
                        self.wall_check[direction]):
                    continue
                next_y, next_x = (
                    current_pos.y + direction.value.y, current_pos.x +
                    direction.value.x)
                neighbor = Vector2D(next_y, next_x)
                cost_to_neighbor = current_cost + 1
                if cost_to_neighbor < distances.get(neighbor, float('inf')):
                    distances[neighbor] = cost_to_neighbor
                    came_from[neighbor] = current_pos
                    heapq.heappush(queue, (cost_to_neighbor, neighbor))
        self.fallback_movement(start)

    def get_path(
            self,
            came_from: dict[Vector2D, Vector2D | None],
            target: Vector2D) -> None:
        current: Vector2D | None = target
        path = []
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()
        if len(path) > 1:
            best_direction = self.get_direction_optimal_path(path[0], path[1])
            self.move_dir = best_direction
            self.move_dir_state = self.best_dir(best_direction)
        else:
            self.fallback_movement(path[0])

    def best_dir(self, vector: Vector2D) -> Direction:
        x, y = vector.x, vector.y

        if x == 0 and y == 0:
            return Direction.ZERO

        if x == 0 and y == 1:
            return Direction.SOUTH

        elif x == 0 and y == -1:
            return Direction.NORTH

        elif x == 1 and y == 0:
            return Direction.EAST

        elif x == -1 and y == 0:
            return Direction.WEST

        return Direction.ZERO

    def get_direction_optimal_path(
            self,
            current: Vector2D,
            next_pos: Vector2D) -> Vector2D:

        diff_y = next_pos.y - current.y
        diff_x = next_pos.x - current.x
        for direction in Direction:
            if direction.value.y == diff_y and direction.value.x == diff_x:
                return direction.value
        return Direction.ZERO.value

    def fallback_movement(self, current_pos: Vector2D) -> None:

        for direction in self.possible_directions:
            if not (
                self.grid[int(current_pos.y)][int(current_pos.x)] &
                    self.wall_check[direction]):
                self.move_dir = direction.value
                return

    def flee_behavior(self) -> None:
        best_direction: Vector2D = Direction.ZERO.value
        best_score = float('-inf')

        pacman_pos = Vector2D(
            self.pacman.current_pos_y, self.pacman.current_pos_x)

        for direction in self.possible_directions:
            if not self.can_move(direction.value):
                continue

            next_pos = Vector2D(
                self.current_pos_y + direction.value.y,
                self.current_pos_x + direction.value.x
            )

            dist_to_pacman = (
                (next_pos.y - pacman_pos.y) ** 2 + (
                    next_pos.x - pacman_pos.x) ** 2)

            score = dist_to_pacman

            if score > best_score:
                best_score = score
                best_direction = direction.value

        self.move_dir = best_direction
        self.move_dir_state = self.best_dir(best_direction)


class Blinky(Ghost):

    def get_target(self) -> Vector2D:
        return Vector2D(self.pacman.current_pos_y, self.pacman.current_pos_x)


class Pinky(Ghost):

    def get_target(self) -> Vector2D:
        target_y = self.pacman.current_pos_y + (self.pacman.move_dir.y * 4)
        target_x = self.pacman.current_pos_x + (self.pacman.move_dir.x * 4)
        return Vector2D(target_y, target_x)


class Inky(Ghost):

    def get_target(self) -> Vector2D:
        target_y = self.pacman.current_pos_y + (self.pacman.move_dir.y * 2)
        target_x = self.pacman.current_pos_x + (self.pacman.move_dir.x * 2)
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
