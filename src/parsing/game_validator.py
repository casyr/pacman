from __future__ import annotations
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
    """Base model for validators that convert settings to dataclasses."""

    @classmethod
    def apply_fallback(
        cls,
        value_setting_name: Any,
        handler: ValidatorFunctionWrapHandler,
        info: ValidationInfo
    ) -> int:
        """Validate a setting or replace it with its declared default.

        Args:
            value_setting_name: Raw setting value to validate.
            handler: Pydantic validation handler for the setting.
            info: Context identifying the field being validated.

        Returns:
            The validated integer value or the field's default.
        """
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
        """Convert validated data to its application settings dataclass.

        Returns:
            The corresponding settings dataclass.
        """
        pass


class LevelValidator(BaseGameValidator):
    """Validate dimensions and defaults for a single level."""

    level_index: int = Field(default=0)
    width: int = Field(default=10, ge=10, le=20)
    height: int = Field(default=10, ge=10, le=20)

    def to_dataclass(self) -> LevelSettings:
        """Create level settings from validated dimensions.

        Returns:
            The validated level settings.
        """
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
        """Validate a level dimension, falling back to its default.

        Args:
            value_setting_name: Raw width or height value.
            handler: Pydantic validation handler for the field.
            info: Context identifying the field being validated.

        Returns:
            The validated dimension or its default value.
        """
        return cls.apply_fallback(value_setting_name, handler, info)

    @model_validator(mode="after")
    def check_missing_fields(self) -> LevelValidator:
        """Log omitted fields and retain their defaults.

        Returns:
            This validated level model.
        """
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
    """Validate game-wide settings and normalize the level list."""

    highscore_filename: str = Field(default="highscore.json")
    levels: list[LevelValidator] = Field(
        default_factory=lambda: [LevelValidator() for _ in range(10)]
    )
    lives: int = Field(default=3, ge=1, le=10)
    pacgum: int = Field(default=42, ge=1)
    super_pacgum: int = Field(default=4, ge=1, le=4)
    points_per_pacgum: int = Field(default=10, ge=1, le=10)
    points_per_super_pacgum: int = Field(default=50, ge=1, le=50)
    points_per_ghost: int = Field(default=200, ge=1, le=200)
    seed: int = Field(default=42, ge=1, le=100)
    level_max_time: int = Field(default=90, ge=40, le=3600)

    def to_dataclass(self) -> GameSettings:
        """Create game settings from validated fields.

        Returns:
            The validated game settings.
        """
        return GameSettings(
            highscore_filename=self.highscore_filename,
            levels=[lvl.to_dataclass() for lvl in self.levels],
            lives=self.lives,
            pacgum=self.pacgum,
            super_pacgum=self.super_pacgum,
            points_per_pacgum=self.points_per_pacgum,
            points_per_super_pacgum=self.points_per_super_pacgum,
            points_per_ghost=self.points_per_ghost,
            seed=self.seed,
            level_max_time=self.level_max_time,
        )

    @field_validator("highscore_filename", mode="before")
    @classmethod
    def check_highscore_extension(cls, name_highscore: Any) -> str:
        """Require a JSON filename for high scores.

        Args:
            name_highscore: Candidate high-score filename.

        Returns:
            The supplied filename or the default JSON filename.
        """
        if (
            not isinstance(name_highscore, str)
            or not name_highscore.lower().endswith(".json")
        ):
            logger.warning(
                f"Invalid highscore filename '{name_highscore}' "
                "(must be a string end with .json). "
                "Falling back to default: 'highscore.json'")
            return "highscore.json"
        return name_highscore

    @staticmethod
    def _check_level_isinstance(levels: Any) -> list[dict[str, Any]]:
        """Keep level entries that are mappings and replace others.

        Args:
            levels: Raw level-list value.

        Returns:
            A list containing only dictionaries.
        """
        if not isinstance(levels, list):
            logger.warning(
                "Levels format is not a list. Resetting to default.")
            return []

        cleaned_levels: list[dict[str, Any]] = []
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
    def adjust_levels_count(cls, levels: Any) -> list[dict[str, Any]]:
        """Normalize level entries to the supported count.

        Args:
            levels: Raw level-list value.

        Returns:
            Ten or more normalized level dictionaries, capped at twenty.
        """
        cleaned_levels: list[dict[str, Any]] = cls._check_level_isinstance(
            levels)

        nb_levels: int = len(cleaned_levels)
        if nb_levels > 20:
            logger.warning(
                f"Too many levels ({nb_levels}). Maximum is 10. Truncating."
            )
            cleaned_levels = cleaned_levels[:20]
        elif nb_levels < 10:
            logger.warning(
                f"Invalid numbers of level '{nb_levels}' it as "
                "to be 10. Replaced with default levels."
                )
            while len(cleaned_levels) < 10:
                cleaned_levels.append({})

        for i, lvl_dict in enumerate(cleaned_levels):
            lvl_dict["level_index"] = i + 1

        return cleaned_levels

    @field_validator(
        "pacgum",
        "super_pacgum",
        "points_per_pacgum",
        "points_per_super_pacgum",
        "points_per_ghost",
        "lives",
        "seed",
        "level_max_time",
        mode="wrap"
    )
    @classmethod
    def validate_game_fields(
            cls,
            value_setting_name: Any,
            handler: ValidatorFunctionWrapHandler,
            info: ValidationInfo) -> int:
        """Validate a game setting, falling back to its default.

        Args:
            value_setting_name: Raw setting value to validate.
            handler: Pydantic validation handler for the field.
            info: Context identifying the field being validated.

        Returns:
            The validated integer value or the field's default.
        """
        return cls.apply_fallback(value_setting_name, handler, info)

    @model_validator(mode="after")
    def check_missing_fields(self) -> GameValidator:
        """Log omitted fields and retain their defaults.

        Returns:
            This validated game model.
        """
        missing_fields = (
            set(self.__class__.model_fields.keys()) - self.model_fields_set)
        for field in missing_fields:
            default_value = getattr(self, field)
            logger.warning(
                f"Missing field : '{field}'. "
                f"Clamped default value : {default_value}"
            )
        return self
