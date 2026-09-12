from .game_session_manager import GameSession, GameStatus
from .maze_adaptater import MazeAdapter


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
        self.super_pacgums: list[tuple[int, int]] = []
        self.ghosts_spawns: list[tuple[int, int]] = []
        self.player_spawn: tuple[int, int] = (0, 0)

    def build_level(self) -> None:
        if self.status == GameStatus.PLAYING:
            seed_to_use = self.seed if self.level_index == 0 else 0
            maze = MazeAdapter(self.width, self.height, seed_to_use)
            self.maze = maze.generate_level()
            self._setup_entities_and_collectibles()

    def _setup_entities_and_collectibles(self) -> None:
        pass
