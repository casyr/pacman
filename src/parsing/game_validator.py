import logging
from pydantic import BaseModel, Field, field_validator
from typing import Any

# from src.exceptions import ParsingError

logger = logging.getLogger(__name__)


class LevelConfig(BaseModel):
    width: int = Field(default=20, ge=10, le=100)
    height: int = Field(default=20, ge=10, le=100)

    @field_validator("width", mode="before")
    @classmethod
    def validate_width(cls, value: Any) -> int:
        if not isinstance(value, int) or value < 5 or value > 100:
            logger.warning(
                f"Invalid width '{value}' (must be between 5 and 100)."
                " Clamped to default: 20")
            return 20
        return value

    @field_validator("height", mode="before")
    @classmethod
    def validate_height(cls, value: Any) -> int:
        if not isinstance(value, int) or value < 5 or value > 100:
            logger.warning(
                f"Invalid height '{value}' (must be between 5 and 100)."
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
    points_per_pacgum: int = Field(default=10, ge=1, le=100)
    points_per_super_pacgum: int = Field(default=50, ge=1, le=100)
    points_per_ghost: int = Field(default=200, ge=1, le=100)
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

    @field_validator("levels", mode="before")
    @classmethod
    def adjust_levels_count(cls, levels: Any) -> Any:
        if isinstance(levels, list):
            original_levels: int = len(levels)
            if len(levels) > 10:
                levels = levels[:10]
                logger.warning(
                    f"Invalid levels numbers there was {original_levels} "
                    "( must be <= 10) Clamped to default: 10 levels")
            while len(levels) < 10:
                levels.append({})
                logger.warning(
                    f"Invalid levels numbers there was {original_levels} "
                    "( must be 10) Clamped to default: 10 levels")
        return levels
