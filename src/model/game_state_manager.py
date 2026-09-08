from src.parsing.game_settings import GameSettings


class GameStateManager:
    def __init__(self, settings: GameSettings) -> None:
        self.settings: GameSettings = settings
        self.total_levels: int = len(settings.levels)
        self.current_score: int = 0
        self.current_level_index: int = 0
        self.lives_remaining: int = settings.lives
        self.time_remaining: int = settings.level_max_time
        self.pacgum_remaining: int = 0
        self.super_pacgum_remaining: int = 0
