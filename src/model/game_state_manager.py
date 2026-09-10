from ..parsing import GameSettings
from enum import Enum, auto
from dataclasses import dataclass


@dataclass
class CheatMode:
    active: bool = False
    invincibility: bool = False
    freeze: bool = False
    speed: bool = False


class GameStatus(Enum):
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    VICTORY = auto()


class GameStateManager:
    def __init__(self, settings: GameSettings) -> None:
        self.settings: GameSettings = settings
        self.total_levels: int = len(settings.levels)
        self.current_level_index: int = 0
        self.current_score: int = 0
        self.lives_remaining: int = settings.lives
        self.time_remaining: float = settings.level_max_time
        self.time_level: float = settings.level_max_time
        self.pacgum_remaining: int = settings.pacgum
        self.super_pacgum_remaining: int = settings.super_pacgum
        self.active_power: bool = False
        self.game_status: GameStatus = GameStatus.PLAYING
        self.cheat_mode: CheatMode = CheatMode()
        self.super_mode: float = 8

    def add_score(self, score: int) -> None:
        self.current_score += score

    def _next_level(self) -> None:
        if self.current_level_index < self.total_levels:
            self.current_level_index += 1
        else:
            self.flags_has_won = True

    def check_level_cleared(self) -> None:
        if self.pacgum_remaining == 0:
            self._next_level()

    def reset_level_data(self) -> None:
        self.time_remaining = self.settings.level_max_time
        self.pacgum_remaining = self.settings.pacgum
        self.super_pacgum_remaining = self.settings.super_pacgum

    def update_timers(self, elapsed_time: float) -> None:
        if self.game_status != GameStatus.PLAYING:
            return
        self.time_remaining = max(0.0, self.time_remaining - elapsed_time)
        if self.time_remaining == 0.0:
            self.flags_game_over = True

    def loose_life(self) -> None:
        if self.cheat_mode.invincibility:
            return
        self.lives_remaining -= 1

    def consume_pacgum(self) -> None:
        self.pacgum_remaining -= 1
        self.add_score(self.settings.points_per_pacgum)
        self.check_level_cleared()

    def consume_super_pacgum(self) -> None:
        self.super_pacgum_remaining -= 1
        self.add_score(self.settings.super_pacgum)
        self.activate_power_mode()

    def activate_power_mode(self) -> None:
        self.active_power = True
        self.time_start_super_mode = self.time_level - self.time_remaining

    def check_activate_power_mode(self) -> None:
        time_passed: float = (
            self.time_start_super_mode - self.time_remaining)
        if time_passed >= self.super_mode:
            self.active_power = False

    def cheat_extra_lives(self) -> None:
        if not self.cheat_mode.active:
            return
        self.lives_remaining = min(self.lives_remaining + 1, 10)

    def cheat_skip_level(self) -> None:
        if not self.cheat_mode.active:
            return
        self.current_level_index = min(self.current_level_index + 1, 10)

    def switch_cheat_mode(self) -> None:
        self.cheat_mode.active = not self.cheat_mode.active

    def switch_invincibility(self) -> None:
        self.cheat_mode.invincibility = not self.cheat_mode.invincibility

    def switch_ghost_freeze(self) -> None:
        self.cheat_mode.freeze = not self.cheat_mode.freeze

    def switch_speed_boost(self) -> None:
        self.cheat_mode.speed = not self.cheat_mode.speed
