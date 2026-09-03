import logging
from pydantic import BaseModel, Field, field_validator, ValidationError
from typing import Any

logger = logging.getLogger(__name__)


class LevelConfig(BaseModel):
    width: int = Field(default=20, ge=10, le=100)
    height: int = Field(default=20, ge=10, le=100)

    @field_validator("width", mode="before")
    @classmethod
    def validate_width(cls, value: Any) -> int:
        if not isinstance(value, int) or value < 10 or value > 100:
            logger.warning(
                f"Invalid width '{value}' (must be between 10 and 100)."
                " Clamped to default: 20")
            return 20
        return value

    @field_validator("height", mode="before")
    @classmethod
    def validate_height(cls, value: Any) -> int:
        if not isinstance(value, int) or value < 10 or value > 100:
            logger.warning(
                f"Invalid height '{value}' (must be between 10 and 100)."
                " Clamped to default: 20")
            return 20
        return value


class GameSettings(BaseModel):
    highscore_filename: str = Field(default="highscore.json")
    levels: list[LevelConfig] = Field(
        default_factory=lambda: [LevelConfig() for _ in range(10)]
    )
    lives: int = Field(default=3, ge=1, le=10)
    # WARNING : MAKE SURE PACGUM FILED MAZE NO IDEA FOR NOW 02/09
    #
    pacgum: int = Field(default=42, ge=1)
    #
    #
    points_per_pacgum: int = Field(default=10, ge=1, le=10)
    points_per_super_pacgum: int = Field(default=50, ge=1, le=50)
    points_per_ghost: int = Field(default=200, ge=1, le=200)
    seed: int = Field(default=42)
    level_max_time: int = Field(default=90, ge=40, le=3600)

    @field_validator("highscore_filename")
    @classmethod
    def check_highscore_extension(cls, name_highscore: str) -> str:
        if not name_highscore.lower().endswith(".json"):
            logger.warning(
                f"Invalid highscore filename '{name_highscore}'  (must "
                "end with .json). Falling back to default: 'highscore.json'")
            return "highscore.json"
        return name_highscore

    @staticmethod
    def _single_level(item: Any) -> LevelConfig:
        if isinstance(item, dict):
            try:
                return LevelConfig.model_validate(item)
            except ValidationError:
                logger.warning(
                    f"Invalid level {item}. Replaced with "
                    "default values. Width and Height = 20"
                )
                return LevelConfig()
        logger.warning(
            f"Invalid level item '{item}'. Replaced with default."
        )
        return LevelConfig()

    @field_validator("levels", mode="before")
    @classmethod
    def adjust_levels_count(cls, levels: Any) -> list[LevelConfig]:
        if not isinstance(levels, list):
            logger.warning(
                "Levels format is not a list. Resetting to default.")
            levels = []

        cleaned_levels: list[LevelConfig] = [
            cls._single_level(item) for item in levels
        ]

        nb_levels: int = len(cleaned_levels)
        if nb_levels > 10:
            cleaned_levels = cleaned_levels[:10]
        if nb_levels < 10:
            logger.warning(
                f"Invalid numbers of level '{nb_levels}'. at least 10"
                "Replaced with default levels."
                )
        while len(cleaned_levels) < 10:
            cleaned_levels.append(LevelConfig())
        return cleaned_levels

    @field_validator("lives", mode="before")
    @classmethod
    def adjust_lives(cls, lives: Any) -> int:
        if not isinstance(lives, int) or lives < 1 or lives > 10:
            logger.warning(
                "Do not try to be God. Lives"
                "(must be > 0 or < 11) Clamped to default: 3 lives")
            return 3
        return lives

    @field_validator("points_per_pacgum", mode="before")
    @classmethod
    def adjust_pacgum_points(cls, pacgum_pts: Any) -> int:
        if not isinstance(pacgum_pts, int) or not (1 <= pacgum_pts <= 10):
            logger.warning(
                "Pacgum_pts (must be > 0 or <= 10) "
                "Clamped to default: 10 pacgum_pts")
            return 10
        return pacgum_pts

    @field_validator("points_per_super_pacgum", mode="before")
    @classmethod
    def adjust_super_pacgum_points(cls, super_pacgum_pts: Any) -> int:
        if (
            not isinstance(super_pacgum_pts, int)
            or not (1 <= super_pacgum_pts <= 50)
        ):
            logger.warning(
                "Collect super_pacgum_pts is fun (must be > 0 or <= 50) "
                "Clamped to default: 50 super_pacgum_pts")
            return 50
        return super_pacgum_pts

    @field_validator("points_per_ghost", mode="before")
    @classmethod
    def adjust_ghost_points(cls, ghost_pts: Any) -> int:
        if not isinstance(ghost_pts, int) or not (1 <= ghost_pts <= 200):
            logger.warning(
                "Collect ghost_pts is fun (must be > 0 or <= 200) "
                "Clamped to default: 200 ghost_pts")
            return 200
        return ghost_pts

    @field_validator("level_max_time", mode="before")
    @classmethod
    def adjust_time(cls, time: Any) -> int:
        if not isinstance(time, int) or not (40 <= time <= 3600):
            logger.warning(
                    "Are you trying to be a time-keeper ? time is precious"
                    "(must be >= 40 or <= 3600) Clamped to default: 90 s")
            return 90
        return time
