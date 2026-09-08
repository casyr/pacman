import sys
import logging
from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
    ValidatorFunctionWrapHandler,
    ValidationInfo,
    ValidationError)
from abc import ABC, abstractmethod
from typing import Any
from .game_settings import LevelSettings, GameSettings

logger = logging.getLogger(__name__)


class BaseGameValidator(BaseModel, ABC):

    @classmethod
    def apply_fallback(
        cls,
        value_setting_name: Any,
        handler: ValidatorFunctionWrapHandler,
        info: ValidationInfo
    ) -> int:
        try:
            validated_value = handler(value_setting_name)
            return int(validated_value)
        except ValidationError as e:
            field_name = str(info.field_name)
            default_val = cls.model_fields[field_name].default
            clean_msg = e.errors()[0]['msg']
            logger.warning(
                f"[{cls.__name__}] {field_name} invalid: {clean_msg}. "
                f"Clamped to default: {default_val}"
            )
            return int(default_val)

    @abstractmethod
    def to_dataclass(self) -> Any:
        pass


class LevelValidator(BaseGameValidator):
    level_index: int = Field(default=0)
    width: int = Field(default=20, ge=10, le=100)
    height: int = Field(default=20, ge=10, le=100)

    def to_dataclass(self) -> LevelSettings:
        return LevelSettings(
            width=self.width,
            height=self.height)

    @field_validator("width", "height", mode="wrap")
    @classmethod
    def validate_level_fields(
            cls,
            value_setting_name: Any,
            handler: ValidatorFunctionWrapHandler,
            info: ValidationInfo) -> int:
        return cls.apply_fallback(value_setting_name, handler, info)

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


class GameValidator(BaseGameValidator):
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

    @field_validator(
        "points_per_pacgum",
        "points_per_super_pacgum",
        "points_per_ghost",
        "lives",
        "level_max_time",
        mode="wrap"
    )
    @classmethod
    def validate_level_fields(
            cls,
            value_setting_name: Any,
            handler: ValidatorFunctionWrapHandler,
            info: ValidationInfo) -> int:
        return cls.apply_fallback(value_setting_name, handler, info)

    @field_validator("seed", mode="before")
    @classmethod
    def adjust_seed(cls, seed: Any) -> int | str:
        if not isinstance(seed, (int, str)):
            logger.warning(
                "Seed must be an integer or string. "
                "Clamped to default: 42")
            return 42
        return seed

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
