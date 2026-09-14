import logging
import random
from .game_session_manager import GameSession, GameStatus
from .maze_adaptater import MazeAdapter
from ..errors import LevelError, GameSettingsError

logger = logging.getLogger(__name__)


class LevelBuilder:

    def __init__(self, current_game: GameSession):
        self.current_game = current_game
        self.width: int = (
            current_game.settings.levels[current_game.level_index].width)
        self.height: int = (
            current_game.settings.levels[current_game.level_index].height)
        self.seed = current_game.settings.seed
        self.level_index = current_game.level_index
        self.pacgum = current_game.settings.pacgum
        self.pacgum_pos: set[tuple[int, int]] = set()
        self.maze: MazeAdapter = MazeAdapter(
            self.width, self.height, self._seed_using(current_game))
        self.super_pacgums_pos: set[tuple[int, int]] = set()
        self.ghosts_pos: list[tuple[int, int]] = []
        self.player_pos: tuple[int, int] = (0, 0)

    def _seed_using(self, current_game: GameSession) -> int:
        seed: int = current_game.settings.seed
        seed_to_use: int = seed if self.level_index == 0 else 0
        return seed_to_use

    def build_level(self) -> None:
        if self.current_game.game_status == GameStatus.PLAYING:
            self.maze.generate_level()
            self._setup_entities_and_collectibles()

    def _setup_entities_and_collectibles(self) -> None:
        self._setup_collectibles_super_pacgums()
        self._setup_entities_ghost()
        self._setup_entities_player()
        self._setup_collectibles_pacgums()

    def _setup_collectibles_super_pacgums(self) -> None:
        corners: list[tuple[int, int]] = [
            (0, 0),
            (0, self.width - 1),
            (self.height - 1, 0),
            (self.height - 1, self.width - 1),
            ]
        for y, x in corners:
            try:
                positions = self._check_first_coordonate(y, x)
                if positions is not None:
                    self.super_pacgums_pos.add(positions)
            except LevelError as err:
                logging.warning(f"{err}Superpacgum")

    def _setup_entities_ghost(self) -> None:
        ignore: set[tuple[int, int]] = set()
        ignore.update(self.super_pacgums_pos)

        corners: list[tuple[int, int]] = [
            (0, 0),
            (0, self.width - 1),
            (self.height - 1, 0),
            (self.height - 1, self.width - 1),
            ]

        for pos_y, pos_x in corners:
            try:
                positions = self._available_space(
                    [(pos_y, pos_x)], {(pos_y, pos_x)}, ignore)
                if positions is not None:
                    self.ghosts_pos.append(positions)
            except LevelError as err:
                logging.warning(f"{err}Ghost")

    def _setup_entities_player(self) -> None:
        ignore: set[tuple[int, int]] = set()

        ignore.update(self.super_pacgums_pos, self.ghosts_pos)
        pos_x: int = self.width // 2
        pos_y: int = self.height // 2
        try:
            positions = self._available_space(
                    [(pos_y, pos_x)], {(pos_y, pos_x)}, ignore)
            if positions is not None:
                self.player_pos = positions
        except LevelError as err:
            raise LevelError(f"{err}Pacman must be present to play")

    def _setup_collectibles_pacgums(self) -> None:
        ignore: set[tuple[int, int]] = set()
        pos_x: int = 0
        pos_y: int = 0

        ignore.update(self.super_pacgums_pos, [self.player_pos])

        while pos_x < self.width:
            pos_x += 1
            pos_y == 0
            while pos_y < self.height:
                if (
                    self.maze.grid[pos_y][pos_x] != 15
                    and (pos_y, pos_x) not in ignore
                ):
                    self.pacgum_pos.add((pos_y, pos_x))
                pos_y += 1
        try:
            if len(self.pacgum_pos) < self.pacgum:
                raise GameSettingsError(
                    f"Requested pacgums {self.pacgum}"
                    " exceeds available positions "
                    f"{len(self.pacgum_pos)}."
                    f"Clamped to default: {len(self.pacgum_pos)} ")
        except GameSettingsError as e:
            logger.warning(f"{e.__class__.__name__} {e}")
            self.pacgum = len(self.pacgum_pos)
            self.current_game.pacgum_remaining = len(self.pacgum_pos)

    def _check_first_coordonate(
            self, pos_y: int, pos_x: int) -> tuple[int, int] | None:

        if self.maze.grid[pos_y][pos_x] != 15:
            return (pos_y, pos_x)
        return self._available_space([(pos_y, pos_x)], {(pos_y, pos_x)}, set())

    def _available_space(
            self,
            queue: list[tuple[int, int]],
            seen: set[tuple[int, int]],
            ignore: set[tuple[int, int]]) -> tuple[int, int] | None:

        directions: list[tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)

        while queue:
            pos_y, pos_x = queue.pop(0)
            if (
                self.maze.grid[pos_y][pos_x] != 15
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
