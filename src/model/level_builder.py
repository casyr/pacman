import logging
import random
from .game_session_manager import GameSession
from .maze_adaptater import MazeAdapter
from .ghost_factory import GhostFactory
from .entities import Ghost, PacMan
from .game_board import GameBoard
from ..shared import GhostName, Vector2D, GridBounds, Direction
from ..errors import LevelError

logger = logging.getLogger(__name__)


class LevelBuilder:

    def __init__(self, current_game: GameSession):
        self.current_game = current_game

    def _seed_using(self, seed: int, level_index: int) -> int:
        seed_to_use: int = seed if level_index == 0 else 0
        return seed_to_use

    def build_level(self) -> GameBoard:
        level_index = self.current_game.level_index
        lvl_data = self.current_game.settings.levels[level_index]
        width = lvl_data.width
        height = lvl_data.height
        bounds = GridBounds(width, height)
        seed = self._seed_using(self.current_game.settings.seed, level_index)

        maze: MazeAdapter = MazeAdapter(
            width,
            height,
            seed)
        maze.generate_level()
        super_pacgums_pos = self._setup_collectibles_super_pacgums(
            maze, bounds)
        player_spawn_pos = self._setup_entities_player_position(
            super_pacgums_pos, maze, bounds)
        player = self._setup_entities_player(player_spawn_pos, maze)
        ghosts_spawn_pos = self._setup_entities_ghost_position(
            super_pacgums_pos, player_spawn_pos, maze, bounds)
        ghosts = self._setup_entities_ghost(ghosts_spawn_pos, maze, player)
        pacgum_pos = self._setup_collectibles_pacgums(
            super_pacgums_pos, player_spawn_pos, maze, bounds)
        self.current_game.pacgum_remaining = len(pacgum_pos)
        self.current_game.super_pacgum_remaining = len(super_pacgums_pos)
        return GameBoard(
            maze=maze,
            player=player,
            player_spawn_pos=player_spawn_pos,
            ghosts=ghosts,
            ghosts_spawn_pos=ghosts_spawn_pos,
            pacgums=self.current_game.pacgum_remaining,
            pacgum_pos=pacgum_pos,
            super_pacgums_pos=super_pacgums_pos,
        )

    def _setup_collectibles_super_pacgums(
            self,
            maze: MazeAdapter,
            bounds: GridBounds
            ) -> set[Vector2D]:

        available_positions: list[Vector2D] = []

        for pos in bounds.corners_pos:
            try:
                positions = self._check_first_coordonate(pos, maze, bounds)
                if positions is not None:
                    available_positions.append(positions)
            except LevelError as err:
                logging.warning(f"{err}Superpacgum")
        super_pacgums_position = (
            self._check_super_pacgum(
                self.current_game.settings.super_pacgum, available_positions)
        )
        return super_pacgums_position

    def _check_super_pacgum(
            self,
            super_pacgum: int,
            available_positions: list[Vector2D]
            ) -> set[Vector2D]:

        total_available: int = len(available_positions)

        if total_available < super_pacgum:
            logging.warning("GameSettingsError: "
                            f"Requested super pacgums {super_pacgum}"
                            f"exceeds available "
                            f"positions {total_available}. "
                            f"Clamped to default: {total_available} ")
            super_pacgum = total_available
        selected_coords = random.sample(available_positions, k=super_pacgum)
        return set(selected_coords)

    def _setup_entities_ghost_position(
            self,
            super_pacgums_pos: set[Vector2D],
            player_spawn_pos: Vector2D,
            maze: MazeAdapter,
            bounds: GridBounds
            ) -> dict[GhostName, Vector2D]:

        ghosts_spawn_pos: dict[GhostName, Vector2D] = {}
        ignore: set[Vector2D] = set()
        ignore.update(super_pacgums_pos)
        ignore.add(player_spawn_pos)

        for name, pos in zip(GhostName, bounds.corners_pos):
            try:
                positions = self._available_space(
                    [pos], {pos}, ignore, maze, bounds)
                if positions is not None:
                    ghosts_spawn_pos[name] = positions
            except LevelError as err:
                logging.warning(f"{err}Ghost")
        return ghosts_spawn_pos

    def _setup_entities_ghost(
            self,
            ghosts_spawn_pos: dict[GhostName, Vector2D],
            maze: MazeAdapter,
            pacman: PacMan
            ) -> dict[GhostName, Ghost]:

        ghosts: dict[GhostName, Ghost] = {}
        for name, pos in ghosts_spawn_pos.items():
            new_ghost = GhostFactory.create(
                name, pos, maze, pacman)
            ghosts[name] = new_ghost
        return ghosts

    def _setup_entities_player_position(
            self,
            super_pacgums_pos: set[Vector2D],
            maze: MazeAdapter,
            bounds: GridBounds
            ) -> Vector2D:
        player_spawn_pos: Vector2D = Vector2D(0, 0)
        ignore: set[Vector2D] = set()
        ignore.update(super_pacgums_pos)

        center_pos = Vector2D(bounds.height // 2, bounds.width // 2)

        try:
            positions = self._available_space(
                    [center_pos], {center_pos}, ignore, maze, bounds)
            if positions is not None:
                player_spawn_pos = positions
            return player_spawn_pos
        except LevelError as err:
            raise LevelError(f"{err}Pacman must be present to play")

    def _setup_entities_player(
            self,
            player_spawn_pos: Vector2D,
            maze: MazeAdapter) -> PacMan:
        return PacMan(player_spawn_pos.y,
                      player_spawn_pos.x,
                      maze)

    def _setup_collectibles_pacgums(
            self,
            super_pacgums_pos: set[Vector2D],
            player_spawn_pos: Vector2D,
            maze: MazeAdapter,
            bounds: GridBounds
            ) -> set[Vector2D]:

        ignore: set[Vector2D] = set()
        available_positions: list[Vector2D] = []
        pos_x: int = 0
        pos_y: int = 0
        ignore.update(super_pacgums_pos)
        ignore.add(player_spawn_pos)
        while pos_x < bounds.width:
            pos_y = 0
            while pos_y < bounds.height:
                current_pos = Vector2D(pos_y, pos_x)
                if (
                    maze.grid[pos_y][pos_x] != 15
                    and current_pos not in ignore
                ):
                    available_positions.append(current_pos)
                pos_y += 1
            pos_x += 1
        pacgums_position = (
            self._check_pacgum(
                self.current_game.settings.pacgum, available_positions)
        )
        return pacgums_position

    def _check_pacgum(
            self,
            pacgum: int,
            available_positions: list[Vector2D]
            ) -> set[Vector2D]:

        total_available: int = len(available_positions)

        if total_available < pacgum:
            logger.warning(
                "GameSettingsError:"
                f"Requested pacgums {pacgum} exceeds available "
                f"positions {len(available_positions)}. "
                f"Clamped to default: {len(available_positions)} ")
            self.current_game.pacgum_remaining = total_available
            pacgum = total_available
        selected_coords = random.sample(available_positions, k=pacgum)
        return set(selected_coords)

    def _check_first_coordonate(
            self,
            pos: Vector2D,
            maze: MazeAdapter,
            bounds: GridBounds) -> Vector2D | None:
        if maze.grid[pos.y][pos.x] != 15:
            return pos
        return self._available_space(
            [pos], {pos}, set(), maze, bounds)

    def _available_space(
            self,
            queue: list[Vector2D],
            seen: set[Vector2D],
            ignore: set[Vector2D],
            maze: MazeAdapter,
            bounds: GridBounds) -> Vector2D | None:

        directions: list[Vector2D] = [
            Direction.NORTH.value,
            Direction.SOUTH.value,
            Direction.WEST.value,
            Direction.EAST.value
        ]
        random.shuffle(directions)

        while queue:
            current_pos = queue.pop(0)
            if (
                maze.grid[current_pos.y][current_pos.x] != 15
                and current_pos not in ignore
            ):
                return current_pos

            for direction in directions:
                ny, nx = (
                    current_pos.y + direction.y, current_pos.x + direction.x)
                next_pos = Vector2D(ny, nx)
                if (0 <= next_pos.y < bounds.height
                        and 0 <= next_pos.x < bounds.width
                        and next_pos not in seen):
                    seen.add(next_pos)
                    queue.append(next_pos)

        raise LevelError("No available space for ")
