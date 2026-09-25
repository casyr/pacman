import logging
import random
from .game_session_manager import GameSession, GameStatus
from .maze_adaptater import MazeAdapter
from .ghost_factory import GhostFactory
from .entities import Ghost, PacMan
from .gameboard import GameBoard
from ..shared import GhostName, Vector2D, GridBounds, Direction
from ..errors import LevelError


logger = logging.getLogger(__name__)


class LevelBuilder:

    def __init__(self, current_game: GameSession):
        self.current_game = current_game
        self._lvl_data = current_game.settings.levels[current_game.level_index]
        self.width = self._lvl_data.width
        self.height = self._lvl_data.height
        self.bounds = GridBounds(self.width, self.height)
        self.level_index = current_game.level_index
        self.seed = self._seed_using(self.current_game.settings.seed)

    def _seed_using(self, seed: int) -> int:
        seed_to_use: int = seed if self.level_index == 0 else 0
        return seed_to_use

    def build_level(self) -> GameBoard:
        if self.current_game.game_status == GameStatus.PLAYING:
            maze: MazeAdapter = MazeAdapter(
                self._lvl_data.width,
                self._lvl_data.height,
                self.seed)
            maze.generate_level()
            super_pacgums_pos = self._setup_collectibles_super_pacgums(maze)
            player_spawn_pos = self._setup_entities_player_position(
                super_pacgums_pos, maze)
            player = self._setup_entities_player(player_spawn_pos, maze)
            ghosts_spawn_pos = self._setup_entities_ghost_position(
                super_pacgums_pos, player_spawn_pos, maze)
            ghosts = self._setup_entities_ghost(ghosts_spawn_pos, maze, player)
            pacgum_pos = self._setup_collectibles_pacgums(
                super_pacgums_pos, player_spawn_pos, maze)
        return GameBoard(
            maze=maze,
            player=player,
            player_spawn_pos=player_spawn_pos,
            ghosts=ghosts,
            ghosts_spawn_pos=ghosts_spawn_pos,
            pacgums=self.current_game.pacgum_remaining,
            pacgums_pos=pacgum_pos,
            super_pacgums_pos=super_pacgums_pos,
        )

    def _setup_collectibles_super_pacgums(
            self,
            maze: MazeAdapter
            ) -> set[Vector2D]:
        super_pacgums_pos: set[Vector2D] = set()

        for pos in self.bounds.corners_pos:
            try:
                positions = self._check_first_coordonate(pos, maze)
                if positions is not None:
                    super_pacgums_pos.add(positions)
            except LevelError as err:
                logging.warning(f"{err}Superpacgum")
        return super_pacgums_pos

    def _setup_entities_ghost_position(
            self,
            super_pacgums_pos: set[Vector2D],
            player_spawn_pos: Vector2D,
            maze: MazeAdapter
            ) -> dict[GhostName, Vector2D]:

        ghosts_spawn_pos: dict[GhostName, Vector2D] = {}
        ignore: set[Vector2D] = set()
        ignore.update(super_pacgums_pos)
        ignore.add(player_spawn_pos)

        for name, pos in zip(GhostName, self.bounds.corners_pos):
            try:
                positions = self._available_space(
                    [pos], {pos}, ignore, maze)
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
            ) -> list[Ghost]:

        ghosts: list[Ghost] = []
        for name, pos in ghosts_spawn_pos.items():
            new_ghost = GhostFactory.create(
                name, pos, maze, pacman, ghosts)
            ghosts.append(new_ghost)
        return ghosts

    def _setup_entities_player_position(
            self,
            super_pacgums_pos: set[Vector2D],
            maze: MazeAdapter
            ) -> Vector2D:
        player_spawn_pos: Vector2D = Vector2D(0, 0)
        ignore: set[Vector2D] = set()
        ignore.update(super_pacgums_pos)

        center_pos = Vector2D(self.height // 2, self.width // 2)

        try:
            positions = self._available_space(
                    [center_pos], {center_pos}, ignore, maze)
            if positions is not None:
                player_spawn_pos = positions
            return player_spawn_pos
        except LevelError as err:
            raise LevelError(f"{err}Pacman must be present to play")

    def _setup_entities_player(
            self,
            player_spawn_pos: Vector2D,
            maze: MazeAdapter) -> PacMan:
        return PacMan(
            player_spawn_pos.y,
            player_spawn_pos.x,
            maze)

    def _setup_collectibles_pacgums(
            self,
            super_pacgums_pos: set[Vector2D],
            player_spawn_pos: Vector2D,
            maze: MazeAdapter
            ) -> set[Vector2D]:

        ignore: set[Vector2D] = set()
        available_positions: list[Vector2D] = []
        pos_x: int = 0
        pos_y: int = 0

        ignore.update(super_pacgums_pos)
        ignore.add(player_spawn_pos)

        while pos_x < self.width:
            pos_y = 0
            while pos_y < self.height:
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

        selected_coords = random.sample(available_positions, k=pacgum)
        return set(selected_coords)

    def _check_first_coordonate(
            self,
            pos: Vector2D,
            maze: MazeAdapter) -> Vector2D | None:
        if maze.grid[pos.y][pos.x] != 15:
            return pos
        return self._available_space(
            [pos], {pos}, set(), maze)

    def _available_space(
            self,
            queue: list[Vector2D],
            seen: set[Vector2D],
            ignore: set[Vector2D],
            maze: MazeAdapter) -> Vector2D | None:

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
                if (
                    0 <= next_pos.y < self.height
                    and 0 <= next_pos.x < self.width
                ):
                    if next_pos not in seen:
                        seen.add(next_pos)
                        queue.append(next_pos)

        raise LevelError("No available space for ")
