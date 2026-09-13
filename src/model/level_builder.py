import logging
from .game_session_manager import GameSession, GameStatus
from .maze_adaptater import MazeAdapter

logger = logging.getLogger(__name__)


class LevelBuilder:

    def __init__(self, current_game: GameSession):
        self.status = current_game.game_status
        self.width: int = (
            current_game.settings.levels[current_game.level_index].width)
        self.height: int = (
            current_game.settings.levels[current_game.level_index].height)
        self.seed = current_game.settings.seed
        self.level_index = current_game.level_index
        self.pacgum = current_game.settings.pacgum
        self.maze: MazeAdapter = MazeAdapter(
            self.width, self.height, self._seed_using(current_game))
        self.super_pacgums: set[tuple[int, int]] = set()
        self.ghosts_spawns: list[tuple[int, int]] = []
        self.player_spawn: tuple[int, int] = (0, 0)

    def _seed_using(self, current_game: GameSession) -> int:
        seed: int = current_game.settings.seed
        seed_to_use: int = seed if self.level_index == 0 else 0
        return seed_to_use

    def build_level(self) -> None:
        if self.status == GameStatus.PLAYING:
            self.maze.generate_level()
            self._setup_entities_and_collectibles()

    def _available_space(
            self, pos_y: int, pos_x: int) -> tuple[int, int] | None:

        if self.maze.grid[pos_y][pos_x] != 15:
            return (pos_y, pos_x)

        queue: list[tuple[int, int]] = [(pos_y, pos_x)]
        seen: set[tuple[int, int]] = {(pos_y, pos_x)}

        while queue:
            y, x = queue.pop(0)
            if self.maze.grid[y][x] != 15:
                return (y, x)
            for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < self.height and 0 <= nx < self.width:
                    if (ny, nx) not in seen:
                        seen.add((ny, nx))
                        queue.append((ny, nx))
        return None

    def _setup_collectibles_super_pacgums(self) -> None:
        corners: list[tuple[int, int]] = [
            (0, 0),
            (0, self.width - 1),
            (self.height - 1, 0),
            (self.height - 1, self.width - 1),
            ]
        for y, x in corners:
            positions = self._available_space(y, x)
            if positions is not None:
                self.super_pacgums.add(positions)

    def _setup_entities_and_collectibles(self) -> None:
        self._setup_collectibles_super_pacgums()
