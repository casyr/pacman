import sys
import logging
from pydantic import (BaseModel, Field, field_validator, model_validator,)
from typing import Any
from parsing.game_settings import LevelSettings, GameSettings

logger = logging.getLogger(__name__)


class LevelValidator(BaseModel):
    level_index: int = Field(default=0)
    width: int = Field(default=20, ge=10, le=100)
    height: int = Field(default=20, ge=10, le=100)

    def to_dataclass(self) -> LevelSettings:
        return LevelSettings(
            width=self.width,
            height=self.height)

    @field_validator("width", mode="before")
    @classmethod
    def validate_width(cls, value: Any) -> int:
        if not isinstance(value, int) or value < 10 or value > 100:
            logger.warning(
                f"Invalid width '{value}' (must be between 10 and 100)."
                " Clamped to default: 20")
            return 20
        return value

    @model_validator(mode="after")
    def check_missing_fields(self) -> 'LevelValidator':
        missing_fields = (
            set(self.__class__.model_fields.keys()) - self.model_fields_set)
        for field in missing_fields:
            default_value = getattr(self, field)
            logger.warning(
                f"[Level {self.level_index}] Missing field : '{field}'. "
                f"Clamped default value : {default_value}"
            )
        return self

    @field_validator("height", mode="before")
    @classmethod
    def validate_height(cls, value: Any) -> int:
        if not isinstance(value, int) or value < 10 or value > 100:
            logger.warning(
                f"Invalid height '{value}' (must be between 10 and 100)."
                " Clamped to default: 20")
            return 20
        return value


class GameValidator(BaseModel):
    highscore_filename: str = Field(default="highscore.json")
    levels: list[LevelValidator] = Field(
        default_factory=lambda: [LevelValidator() for _ in range(10)]
    )
    lives: int = Field(default=3, ge=1, le=10)
    # WARNING : MAKE SURE PACGUM FILED MAZE INSIDE MODEL AND
    # DISPLAY MESSAGE IF PACGUM NOT FIT 03/09
    #
    pacgum: int = Field(default=42)
    #
    #
    points_per_pacgum: int = Field(default=10, ge=1, le=10)
    points_per_super_pacgum: int = Field(default=50, ge=1, le=50)
    points_per_ghost: int = Field(default=200, ge=1, le=200)
    seed: int | str = Field(default=42)
    level_max_time: int = Field(default=90, ge=40, le=3600)

    def to_dataclass(self) -> GameSettings:
        return GameSettings(
            highscore_filename=self.highscore_filename,
            levels=[lvl.to_dataclass() for lvl in self.levels],
            lives=self.lives,
            pacgum=self.pacgum,
            points_per_pacgum=self.points_per_pacgum,
            points_per_super_pacgum=self.points_per_super_pacgum,
            points_per_ghost=self.points_per_ghost,
            seed=self.seed,
            level_max_time=self.level_max_time,
        )

    @field_validator("highscore_filename", mode="before")
    @classmethod
    def check_highscore_extension(cls, name_highscore: Any) -> str:
        if (
            not isinstance(name_highscore, str)
            or not name_highscore.lower().endswith(".json")
        ):
            logger.warning(
                f"Invalid highscore filename '{name_highscore}' "
                "(must be a string end with .json). "
                "Falling back to default: 'highscore.json'")
            return "highscore.json"
        elif sys.argv[1] == name_highscore:
            logger.warning(
                f"Filename already used '{name_highscore}' "
                "Falling back to default: 'highscore.json'")
            return "highscore.json"
        return name_highscore

    @staticmethod
    def _check_level_isinstance(levels: Any) -> list[dict]:
        if not isinstance(levels, list):
            logger.warning(
                "Levels format is not a list. Resetting to default.")
            return []

        cleaned_levels: list[dict] = []
        for item in levels:
            if isinstance(item, dict):
                cleaned_levels.append(item)
            else:
                logger.warning(
                    f"Invalid level item '{item}'.")
                cleaned_levels.append({})
        return cleaned_levels

    @field_validator("levels", mode="before")
    @classmethod
    def adjust_levels_count(cls, levels: Any) -> list[dict]:
        cleaned_levels: list[dict] = cls._check_level_isinstance(levels)

        nb_levels: int = len(cleaned_levels)
        if nb_levels > 10:
            cleaned_levels = cleaned_levels[:10]
        if nb_levels < 10:
            logger.warning(
                f"Invalid numbers of level '{nb_levels}' at least 10 "
                "Replaced with default levels."
                )

        while len(cleaned_levels) < 10:
            cleaned_levels.append({})

        for i, lvl_dict in enumerate(cleaned_levels):
            lvl_dict["level_index"] = i + 1

        return cleaned_levels

    @field_validator("lives", mode="before")
    @classmethod
    def adjust_lives(cls, lives: Any) -> int:
        if not isinstance(lives, int) or lives < 1 or lives > 10:
            logger.warning(
                "Lives must be a positif integer "
                "> 0 or < 11. Clamped to default: 3 lives")
            return 3
        return lives

    @field_validator("pacgum", mode="before")
    @classmethod
    def make_sure_pacgum_integer(cls, pacgum: Any) -> int:
        if not isinstance(pacgum, int) or pacgum < 1:
            logger.warning(
                "Pacgum must be a positif integer > 0. "
                "Clamped to default integer")
            return 1
        return pacgum

    @field_validator("points_per_pacgum", mode="before")
    @classmethod
    def adjust_pacgum_points(cls, pacgum_pts: Any) -> int:
        if not isinstance(pacgum_pts, int) or not (1 <= pacgum_pts <= 10):
            logger.warning(
                "Pacgum_pts must be a positif integer > 0 or <= 10. "
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
                "Super_pacgum_pts must be a positif integer > 0 or <= 50. "
                "Clamped to default: 50 super_pacgum_pts")
            return 50
        return super_pacgum_pts

    @field_validator("points_per_ghost", mode="before")
    @classmethod
    def adjust_ghost_points(cls, ghost_pts: Any) -> int:
        if not isinstance(ghost_pts, int) or not (1 <= ghost_pts <= 200):
            logger.warning(
                "Ghost_pts must be a postif integer > 0 or <= 200). "
                "Clamped to default: 200 ghost_pts")
            return 200
        return ghost_pts

    @field_validator("seed", mode="before")
    @classmethod
    def adjust_seed(cls, seed: Any) -> int | str:
        if not isinstance(seed, (int, str)):
            logger.warning(
                "Seed must be an integer or string. "
                "Clamped to default: 42")
            return 42
        return seed

    @field_validator("level_max_time", mode="before")
    @classmethod
    def adjust_time(cls, time: Any) -> int:
        if not isinstance(time, int) or not (40 <= time <= 3600):
            logger.warning(
                    "Level_max_time must be a positif intger"
                    " >= 40 or <= 3600. Clamped to default: 90 s")
            return 90
        return time

    @model_validator(mode="after")
    def check_missing_fields(self) -> 'GameValidator':
        missing_fields = (
            set(self.__class__.model_fields.keys()) - self.model_fields_set)
        for field in missing_fields:
            default_value = getattr(self, field)
            logger.warning(
                f"Missing field : '{field}'. "
                f"Clamped default value : {default_value}"
            )
        return self
