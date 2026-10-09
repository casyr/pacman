from enum import Enum, auto
from dataclasses import dataclass
from ..parsing import GameSettings


@dataclass
class CheatMode:
    """Store enabled cheats and the score granted by the score cheat."""

    invincibility: bool = False
    freeze: bool = False
    speed: bool = False
    score: int = 100


class GameStatus(Enum):
    """Possible states of a game session."""

    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    VICTORY = auto()


class GameSession:
    """Track level progress, score, timers, lives, and game state."""

    def __init__(self, settings: GameSettings) -> None:
        """Initialize a session from validated game settings.

        Args:
            settings: Configuration used for this game session.
        """
        self.settings: GameSettings = settings
        self.total_levels: int = len(settings.levels)
        self.level_index: int = 0
        self.score: int = 0
        self.lives_remaining: int = settings.lives
        self.speed_multiplier: int = 4

        self.time_remaining: float = float(settings.level_max_time)
        self.pacgum_remaining: int = settings.pacgum
        self.super_pacgum_remaining: int = settings.super_pacgum

        self.active_power: bool = False
        self.power_just_expired: bool = False
        self.super_mode_timer: float = 6

        self.game_status: GameStatus = GameStatus.PLAYING
        self.cheat_mode: CheatMode = CheatMode()

        self.player_name: str = ""

    def add_score(self, score: int) -> None:
        """Add a nonnegative amount to the score, up to its maximum.

        Args:
            score: Points to add.
        """
        self.score += max(0, score)
        self.score = min(self.score, 999999999)

    def _next_level(self) -> None:
        """Advance to the next level or mark the session victorious."""
        if self.level_index + 1 < self.total_levels:
            self.level_index += 1
            self.update_level_data()
        else:
            self.game_status = GameStatus.VICTORY

    def check_level_cleared(self) -> None:
        """Advance when no regular or super pacgums remain."""
        if self.pacgum_remaining <= 0 and self.super_pacgum_remaining <= 0:
            self._next_level()

    def reset_cheats(self) -> None:
        """Disable all cheats and restore the default speed multiplier."""
        self.cheat_mode.invincibility = False
        self.cheat_mode.freeze = False
        self.cheat_mode.speed = False
        self.speed_multiplier = 1

    def update_level_data(self) -> None:
        """Reset state that is specific to the active level."""
        self.game_status = GameStatus.PLAYING
        self.active_power = False
        self.super_mode_timer = 0.0
        self.reset_cheats()

    def reset_level_data(self) -> None:
        """Reset session progress and restore initial player resources."""
        self.level_index = 0
        self.score = 0
        self.time_remaining = float(self.settings.level_max_time)
        self.lives_remaining = self.settings.lives
        self.update_level_data()

    def update_timers(self, elapsed_time: float) -> None:
        """Decrease active timers and update timeout or power state.

        Args:
            elapsed_time: Time elapsed since the previous update.
        """
        if self.game_status != GameStatus.PLAYING:
            return
        self.power_just_expired = False
        self.time_remaining = max(0.0, self.time_remaining - elapsed_time)
        if self.time_remaining == 0.0:
            self.game_status = GameStatus.GAME_OVER

        if self.active_power:
            self.super_mode_timer = max(
                0.0, self.super_mode_timer - elapsed_time)
            if self.super_mode_timer == 0.0:
                self.active_power = False
                self.power_just_expired = True

    def activate_power_mode(self) -> None:
        """Enable powered mode and reset its duration."""
        self.super_mode_timer = 6
        self.power_just_expired = False
        self.active_power = True

    def lose_life(self) -> bool:
        """Remove a life and end the game if none remain.

        Returns:
            Always true after processing the lost life.
        """
        self.lives_remaining -= 1
        if self.lives_remaining <= 0:
            self.game_status = GameStatus.GAME_OVER
        return True

    def consume_pacgum(self) -> None:
        """Consume a regular pacgum and award its configured points."""
        if self.pacgum_remaining > 0:
            self.pacgum_remaining -= 1
            self.add_score(self.settings.points_per_pacgum)

    def consume_super_pacgum(self) -> None:
        """Consume a super pacgum, award points, and activate power mode."""
        if self.super_pacgum_remaining > 0:
            self.super_pacgum_remaining -= 1
            self.add_score(self.settings.points_per_super_pacgum)
            self.activate_power_mode()

    def consume_ghost(self) -> None:
        """Award ghost points when power mode is active."""
        if self.active_power:
            self.add_score(self.settings.points_per_ghost)

    def switch_status_paused(self) -> None:
        """Toggle the session between playing and paused states."""
        if self.game_status == GameStatus.PLAYING:
            self.game_status = GameStatus.PAUSED
        elif self.game_status == GameStatus.PAUSED:
            self.game_status = GameStatus.PLAYING

    def cheat_extra_lives(self) -> None:
        """Grant one extra life, up to the configured cap of ten."""
        self.lives_remaining = min(self.lives_remaining + 1, 10)

    def cheat_skip_level(self) -> None:
        """Advance to the next level using normal level progression."""
        self._next_level()

    def cheat_add_score(self) -> None:
        """Add the score amount configured for the score cheat."""
        self.add_score(self.cheat_mode.score)

    def switch_invincibility(self) -> None:
        """Toggle player invincibility."""
        self.cheat_mode.invincibility = not self.cheat_mode.invincibility

    def switch_ghost_freeze(self) -> None:
        """Toggle the ghost freeze cheat."""
        self.cheat_mode.freeze = not self.cheat_mode.freeze

    def switch_speed_boost(self) -> None:
        """Toggle the speed cheat and update the movement multiplier."""
        self.cheat_mode.speed = not self.cheat_mode.speed
        if self.cheat_mode.speed:
            self.speed_multiplier = 2
        if not self.cheat_mode.speed:
            self.speed_multiplier = 1
