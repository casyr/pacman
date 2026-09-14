from enum import Enum, auto
from dataclasses import dataclass
from ..parsing import GameSettings


@dataclass
class CheatMode:
    invincibility: bool = False
    freeze: bool = False
    speed: bool = False


class GameStatus(Enum):
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    VICTORY = auto()


class GameSession:

    def __init__(self, settings: GameSettings) -> None:
        self.settings: GameSettings = settings
        self.total_levels: int = len(settings.levels)
        self.level_index: int = 0
        self.score: int = 0
        self.lives_remaining: int = settings.lives

        self.time_remaining: float = settings.level_max_time
        self.pacgum_remaining: int = settings.pacgum
        self.super_pacgum_remaining: int = settings.super_pacgum

        self.active_power: bool = False
        self.super_mode_timer: float = 0
        self.super_mode_duration: float = 8

        self.game_status: GameStatus = GameStatus.PLAYING
        self.cheat_mode: CheatMode = CheatMode()

    def add_score(self, score: int) -> None:
        self.score += max(0, score)

    def _next_level(self) -> None:
        if self.level_index + 1 < self.total_levels:
            self.level_index += 1
            self.reset_level_data()
        else:
            self.game_status = GameStatus.VICTORY

    def check_level_cleared(self) -> None:
        if self.pacgum_remaining <= 0 and self.super_pacgum_remaining <= 0:
            self._next_level()

    def reset_level_data(self) -> None:
        self.time_remaining = float(self.settings.level_max_time)
        self.pacgum_remaining = self.settings.pacgum
        self.super_pacgum_remaining = self.settings.super_pacgum
        self.active_power = False
        self.super_mode_timer = 0.0

    def update_timers(self, elapsed_time: float) -> None:
        if self.game_status != GameStatus.PLAYING:
            return

        self.time_remaining = max(0.0, self.time_remaining - elapsed_time)
        if self.time_remaining == 0.0:
            self.game_status = GameStatus.GAME_OVER

        if self.active_power:
            self.super_mode_timer = max(
                0.0, self.super_mode_duration - elapsed_time)
            if self.super_mode_timer == 0.0:
                self.active_power = False

    def activate_power_mode(self) -> None:
        self.active_power = True

    def lose_life(self) -> None:
        if self.cheat_mode.invincibility:
            return
        self.lives_remaining -= 1
        if self.lives_remaining <= 0:
            self.game_status = GameStatus.GAME_OVER

    def consume_pacgum(self) -> None:
        if self.pacgum_remaining > 0:
            self.pacgum_remaining -= 1
            self.add_score(self.settings.points_per_pacgum)
            self.check_level_cleared()

    def consume_super_pacgum(self) -> None:
        if self.super_pacgum_remaining > 0:
            self.super_pacgum_remaining -= 1
            self.add_score(self.settings.points_per_super_pacgum)
            self.activate_power_mode()
            self.check_level_cleared()

    def consume_ghost(self) -> None:
        if self.active_power:
            self.add_score(self.settings.points_per_ghost)

    def cheat_extra_lives(self) -> None:
        self.lives_remaining = min(self.lives_remaining + 1, 10)

    def cheat_skip_level(self) -> None:
        self._next_level()

    def switch_invincibility(self) -> None:
        self.cheat_mode.invincibility = not self.cheat_mode.invincibility

    def switch_ghost_freeze(self) -> None:
        self.cheat_mode.freeze = not self.cheat_mode.freeze

    def switch_speed_boost(self) -> None:
        self.cheat_mode.speed = not self.cheat_mode.speed

    def switch_status_paused(self) -> None:
        if self.game_status == GameStatus.PLAYING:
            GameStatus.PAUSED
        elif self.game_status == GameStatus.PAUSED:
            GameStatus.PLAYING
