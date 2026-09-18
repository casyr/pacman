import logging
import random
from .game_session_manager import GameSession, GameStatus
from .maze_adaptater import MazeAdapter
from .ghost_factory import GhostFactory
from .entities import Ghost, PacMan, GhostName
from .gameboard import GameBoard
from ..errors import LevelError

logger = logging.getLogger(__name__)


class LevelBuilder:

    def __init__(self, current_game: GameSession):
        self.current_game = current_game
        self._lvl_data = current_game.settings.levels[current_game.level_index]
        self.width = self._lvl_data.width
        self.height = self._lvl_data.height
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
            pacgums = self.current_game.settings.pacgum
            pacgum_available = self._setup_collectibles_pacgums(
                super_pacgums_pos, player_spawn_pos, maze)
            pacgum_pos = self._check_pacgum(pacgums, pacgum_available)
        return GameBoard(
            maze=maze,
            player=player,
            player_spawn_pos=player_spawn_pos,
            ghosts=ghosts,
            ghosts_spawn_pos=ghosts_spawn_pos,
            pacgums=pacgums,
            pacgum_pos=pacgum_pos,
            super_pacgums_pos=super_pacgums_pos,
        )

    def _setup_collectibles_super_pacgums(
            self,
            maze: MazeAdapter
            ) -> set[tuple[int, int]]:
        super_pacgums_pos: set[tuple[int, int]] = set()
        corners: list[tuple[int, int]] = [
            (0, 0),
            (0, self.width - 1),
            (self.height - 1, 0),
            (self.height - 1, self.width - 1),
            ]
        for y, x in corners:
            try:
                positions = self._check_first_coordonate(y, x, maze)
                if positions is not None:
                    super_pacgums_pos.add(positions)
            except LevelError as err:
                logging.warning(f"{err}Superpacgum")
        return super_pacgums_pos

    def _setup_entities_ghost_position(
            self,
            super_pacgums_pos: set[tuple[int, int]],
            player_spawn_pos: tuple[int, int],
            maze: MazeAdapter
            ) -> dict[GhostName, tuple[int, int]]:

        ghosts_spawn_pos: dict[GhostName, tuple[int, int]] = {}
        ignore: set[tuple[int, int]] = set()
        ignore.update(super_pacgums_pos)
        ignore.add(player_spawn_pos)

        corners: list[tuple[int, int]] = [
            (0, 0),
            (0, self.width - 1),
            (self.height - 1, 0),
            (self.height - 1, self.width - 1),
            ]

        for name, (pos_y, pos_x) in zip(GhostName, corners):
            try:
                positions = self._available_space(
                    [(pos_y, pos_x)], {(pos_y, pos_x)}, ignore, maze)
                if positions is not None:
                    ghosts_spawn_pos[name] = positions
            except LevelError as err:
                logging.warning(f"{err}Ghost")
        return ghosts_spawn_pos

    def _setup_entities_ghost(
            self,
            ghosts_spawn_pos: dict[GhostName, tuple[int, int]],
            maze: MazeAdapter,
            pacman: PacMan
            ) -> list[Ghost]:

        ghosts: list[Ghost] = []
        for name, (pos_y, pos_x) in ghosts_spawn_pos.items():
            new_ghost = GhostFactory.create(
                name, pos_y, pos_x, maze, pacman, ghosts)
            ghosts.append(new_ghost)
        return ghosts

    def _setup_entities_player_position(
            self,
            super_pacgums_pos: set[tuple[int, int]],
            maze: MazeAdapter
            ) -> tuple[int, int]:
        player_spawn_pos: tuple[int, int] = (0, 0)
        ignore: set[tuple[int, int]] = set()
        ignore.update(super_pacgums_pos)

        pos_x: int = self.width // 2
        pos_y: int = self.height // 2
        try:
            positions = self._available_space(
                    [(pos_y, pos_x)], {(pos_y, pos_x)}, ignore, maze)
            if positions is not None:
                player_spawn_pos = positions
            return player_spawn_pos
        except LevelError as err:
            raise LevelError(f"{err}Pacman must be present to play")

    def _setup_entities_player(
            self,
            player_spawn_pos: tuple[int, int],
            maze: MazeAdapter) -> PacMan:
        return PacMan(
            player_spawn_pos[0],
            player_spawn_pos[1],
            maze)

    def _setup_collectibles_pacgums(
            self,
            super_pacgums_pos: set[tuple[int, int]],
            player_spawn_pos: tuple[int, int],
            maze: MazeAdapter
            ) -> list[tuple[int, int]]:

        ignore: set[tuple[int, int]] = set()
        available_positions: list[tuple[int, int]] = []
        pos_x: int = 0
        pos_y: int = 0

        ignore.update(super_pacgums_pos, [player_spawn_pos])

        while pos_x < self.width:
            pos_y = 0
            while pos_y < self.height:
                if (
                    maze.grid[pos_y][pos_x] != 15
                    and (pos_y, pos_x) not in ignore
                ):
                    available_positions.append((pos_y, pos_x))
                pos_y += 1
            pos_x += 1
        return available_positions

    def _check_pacgum(
            self,
            pacgum: int,
            available_positions: list[tuple[int, int]]
            ) -> set[tuple[int, int]]:

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
            pos_y: int,
            pos_x: int,
            maze: MazeAdapter) -> tuple[int, int] | None:
        if maze.grid[pos_y][pos_x] != 15:
            return (pos_y, pos_x)
        return self._available_space(
            [(pos_y, pos_x)], {(pos_y, pos_x)}, set(), maze)

    def _available_space(
            self,
            queue: list[tuple[int, int]],
            seen: set[tuple[int, int]],
            ignore: set[tuple[int, int]],
            maze: MazeAdapter) -> tuple[int, int] | None:

        directions: list[tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)

        while queue:
            pos_y, pos_x = queue.pop(0)
            if (
                maze.grid[pos_y][pos_x] != 15
                and (pos_y, pos_x) not in ignore
            ):
                return (pos_y, pos_x)

            for dy, dx in directions:
                ny, nx = pos_y + dy, pos_x + dx
                if 0 <= ny < self.height and 0 <= nx < self.width:
                    if (ny, nx) not in seen:
                        seen.add((ny, nx))
                        queue.append((ny, nx))

        raise LevelError("No available space for ")
