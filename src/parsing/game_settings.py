from dataclasses import dataclass


@dataclass(frozen=True)
class LevelSettings:
    """Immutable dimensions for one game level."""

    width: int
    height: int


@dataclass(frozen=True)
class GameSettings:
    """Immutable gameplay and scoring configuration."""

    highscore_filename: str
    levels: list[LevelSettings]
    lives: int
    pacgum: int
    super_pacgum: int
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int
    seed: int
    level_max_time: int
