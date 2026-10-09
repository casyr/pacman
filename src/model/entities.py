import heapq
import logging
from abc import ABC, abstractmethod
from ..shared import Direction, GhostState, Vector2D, Wall
from .maze_adaptater import MazeAdapter


logger = logging.getLogger(__name__)


class Entity(ABC):
    """Common position and movement state for maze entities."""

    def __init__(
            self,
            current_y: int,
            current_x: int,
            maze: MazeAdapter) -> None:
        """Initialize entity coordinates and movement state.

        Args:
            current_y: Initial row in the maze.
            current_x: Initial column in the maze.
            maze: Maze providing the grid and its dimensions.
        """

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
        self.speed: float = 0
        self.move_timer: float = 0.0
        self.center_tolerance: float = 0.05

    def respawn(self) -> None:
        """Restore the entity to its spawn position and stop its movement."""
        self.current_pos_y = self.spawn_pos.y
        self.current_pos_x = self.spawn_pos.x
        self.move_pixel_y = float(self.spawn_pos.y)
        self.move_pixel_x = float(self.spawn_pos.x)
        self.move_dir = Direction.ZERO.value
        self.previous_pos = self.spawn_pos
        self.is_dying: bool = False

    def can_move(self, direction: Vector2D) -> bool:
        """Check whether the entity can move in a direction.

        Args:
            direction: Direction vector to check.

        Returns:
            Whether the current tile permits movement that way.
        """

        move_masks: dict[Vector2D, int] = {
            Direction.NORTH.value: Wall.NORTH.value,
            Direction.SOUTH.value: Wall.SOUTH.value,
            Direction.WEST.value: Wall.WEST.value,
            Direction.EAST.value: Wall.EAST.value,
        }

        mask = move_masks.get(direction)
        if mask is None:
            return False

        cell_value: int = (self.grid[self.current_pos_y]
                           [self.current_pos_x])
        return not (cell_value & mask)

    def move_continuously(self, elapsed_time: float) -> None:
        """Advance the entity's pixel position by elapsed time.

        Args:
            elapsed_time: Time elapsed since the previous update.
        """
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

    def is_moving(self) -> bool:
        """Check whether the entity can currently move.

        Returns:
            Whether its current direction is nonzero and unobstructed.
        """
        if self.move_dir == Direction.ZERO.value:
            return False
        return self.can_move(self.move_dir)

    def is_at_intersection(self) -> bool:
        """Check whether the entity is aligned with its current tile.

        Returns:
            Whether both pixel coordinates are within center tolerance.
        """
        return (
            abs(self.move_pixel_y - self.current_pos_y) < self.center_tolerance
            and
            abs(self.move_pixel_x - self.current_pos_x) < self.center_tolerance
        )

    def perfectly_aligns(self) -> None:
        """Snap the pixel coordinates to the current tile coordinates."""
        self.move_pixel_y = float(self.current_pos_y)
        self.move_pixel_x = float(self.current_pos_x)

    @abstractmethod
    def update(self, elapsed_time: float) -> None:
        """Update the entity for one time step.

        Args:
            elapsed_time: Time elapsed since the previous update.
        """


class PacMan(Entity):
    """Player-controlled character and its movement state."""

    def __init__(
            self,
            y: int,
            x: int,
            maze: MazeAdapter) -> None:
        """Initialize Pac-Man at a maze position.

        Args:
            y: Initial row in the maze.
            x: Initial column in the maze.
            maze: Maze providing the grid and its dimensions.
        """
        super().__init__(y, x, maze)
        self.speed = 2
        self.desired_dir: Vector2D = Direction.ZERO.value
        self.desired_state_dir = Direction.ZERO
        self.is_dying: bool = False
        self.death_elapsed: float = 0.0
        self.death_duration: float = 1.6
        self.animation_timer: float = 0.0

    def start_death_animation(self) -> None:
        """Begin the death animation and stop movement."""
        self.is_dying = True
        self.death_elapsed = 0.0
        self.move_dir = Direction.ZERO.value

    def death_animation_finished(self) -> bool:
        """Check whether the death animation duration has elapsed.

        Returns:
            Whether the death animation is complete.
        """
        return self.death_elapsed >= self.death_duration

    def set_direction(self, direction: Direction) -> None:
        """Set Pac-Man's requested movement direction.

        Args:
            direction: Direction requested by the player.
        """
        self.desired_dir = direction.value
        self.desired_state_dir = direction

    def is_reversing(self) -> bool:
        """Check whether the requested direction reverses current movement.

        Returns:
            Whether the requested direction is opposite the current one.
        """
        return (
            self.desired_dir.y == -self.move_dir.y
            and self.desired_dir.x == -self.move_dir.x
        )

    def handle_death_animation(self, elapsed_time: float) -> None:
        """Advance the death timer and reset the animation timer.

        Args:
            elapsed_time: Time elapsed since the previous update.
        """
        self.death_elapsed += elapsed_time
        self.animation_timer = 0.0

    def update(self, elapsed_time: float) -> None:
        """Update animation and movement for one time step.

        Args:
            elapsed_time: Time elapsed since the previous update.
        """

        if self.is_dying:
            self.handle_death_animation(elapsed_time)
            return

        if self.is_moving():
            self.death_elapsed = 0.0
            self.animation_timer += elapsed_time

        if self.is_reversing() and self.can_move(self.desired_dir):
            self.move_dir = self.desired_dir
            self.move_dir_state = self.desired_state_dir

        if (
            self.is_at_intersection()
            and self.desired_dir != self.move_dir
            and self.can_move(self.desired_dir)
        ):
            self.move_dir = self.desired_dir
            self.move_dir_state = self.desired_state_dir
            self.perfectly_aligns()

        self.move_continuously(elapsed_time)


class Ghost(Entity, ABC):
    """Base class for ghosts with chase and flee behavior."""

    def __init__(
            self,
            y: int,
            x: int,
            maze: MazeAdapter,
            pacman: PacMan
            ) -> None:
        """Initialize a ghost and its relationship to Pac-Man.

        Args:
            y: Initial row in the maze.
            x: Initial column in the maze.
            maze: Maze providing the grid and its dimensions.
            pacman: Player character the ghost tracks.
        """
        super().__init__(y, x, maze)
        self.pacman: PacMan = pacman
        self.state: GhostState = GhostState.NORMAL
        self.respawn_timer: float = 0.0
        self.decision_made_on_tile: Vector2D | None = None
        self.animation_timer: float = 0.0
        self.speed: float = 1.5
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
        """Mark the ghost as eaten until its respawn delay expires.

        Args:
            respawn_delay: Seconds to wait before respawning.
        """
        self.state = GhostState.EATEN
        self.respawn_timer = respawn_delay

    def respawn(self) -> None:
        """Restore the ghost to its spawn state."""
        super().respawn()
        self.state = GhostState.NORMAL
        self.respawn_timer = 0.0
        self.decision_made_on_tile = None

    def update(self, elapsed_time: float) -> None:
        """Update ghost timers, decisions, and movement.

        Args:
            elapsed_time: Time elapsed since the previous update.
        """
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
        """Return the tile this ghost should pursue.

        Returns:
            Target tile coordinates.
        """

    def chase_behavior(
            self,
            current_pos_y: int,
            current_pos_x: int,
            target: Vector2D) -> None:
        """Find a shortest path and select its first movement direction.

        Args:
            current_pos_y: Current row of the ghost.
            current_pos_x: Current column of the ghost.
            target: Tile the ghost is pursuing.
        """

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
                if (self.grid[current_pos.y][current_pos.x] &
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
        """Reconstruct a path and select its first step.

        Args:
            came_from: Map of each visited tile to its predecessor.
            target: Destination tile for the path.
        """
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
        """Convert a unit movement vector to its direction enum.

        Args:
            vector: Movement vector to convert.

        Returns:
            Matching cardinal direction, or zero for an unknown vector.
        """
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
        """Get the direction vector from one adjacent tile to another.

        Args:
            current: Starting tile coordinates.
            next_pos: Next tile coordinates in the path.

        Returns:
            Unit vector toward the next tile, or zero if not adjacent.
        """

        diff_y = next_pos.y - current.y
        diff_x = next_pos.x - current.x
        for direction in Direction:
            if direction.value.y == diff_y and direction.value.x == diff_x:
                return direction.value
        return Direction.ZERO.value

    def fallback_movement(self, current_pos: Vector2D) -> None:
        """Choose the first available direction from a tile.

        Args:
            current_pos: Tile from which to choose movement.
        """

        for direction in self.possible_directions:
            if not (
                self.grid[current_pos.y][current_pos.x] &
                    self.wall_check[direction]):
                self.move_dir = direction.value
                return

    def flee_behavior(self) -> None:
        """Choose an available direction that maximizes distance.

        The chosen direction moves the ghost farther from Pac-Man.
        """
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
    """Ghost that targets Pac-Man's current tile."""

    def get_target(self) -> Vector2D:
        """Return Pac-Man's current tile.

        Returns:
            Pac-Man's current row and column.
        """
        return Vector2D(self.pacman.current_pos_y, self.pacman.current_pos_x)


class Pinky(Ghost):
    """Ghost that targets a tile four steps ahead of Pac-Man."""

    def get_target(self) -> Vector2D:
        """Return a tile four steps ahead of Pac-Man.

        Returns:
            Projected target row and column.
        """
        target_y = self.pacman.current_pos_y + (self.pacman.move_dir.y * 4)
        target_x = self.pacman.current_pos_x + (self.pacman.move_dir.x * 4)
        return Vector2D(target_y, target_x)


class Inky(Ghost):
    """Ghost that targets a tile two steps ahead of Pac-Man."""

    def get_target(self) -> Vector2D:
        """Return a tile two steps ahead of Pac-Man.

        Returns:
            Projected target row and column.
        """
        target_y = self.pacman.current_pos_y + (self.pacman.move_dir.y * 2)
        target_x = self.pacman.current_pos_x + (self.pacman.move_dir.x * 2)
        return Vector2D(target_y, target_x)


class Clyde(Ghost):
    """Ghost that retreats when near Pac-Man and chases when far away."""

    def get_target(self) -> Vector2D:
        """Select Clyde's spawn tile nearby, otherwise Pac-Man's tile.

        Returns:
            The selected target row and column.
        """
        dist_case = (
            abs(self.current_pos_y - self.pacman.current_pos_y) +
            abs(self.current_pos_x - self.pacman.current_pos_x)
        )
        if dist_case < 4:
            return self.spawn_pos
        else:
            return Vector2D(
                self.pacman.current_pos_y, self.pacman.current_pos_x)
