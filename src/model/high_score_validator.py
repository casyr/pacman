import logging
from typing import Any
from pydantic import (BaseModel, Field, field_validator)

logger = logging.getLogger(__name__)


class HighScore(BaseModel):
    """Validated player name and score record."""

    player: str = Field(default="player1")
    score: int = Field(default=0)

    @staticmethod
    def _handle_player_names(player: str) -> bool:
        """Check that a player name contains allowed characters.

        Args:
            player: Name to validate.

        Returns:
            Whether the name is at most ten characters and allowed.
        """
        cleaned = player.strip()
        if len(player) > 10:
            return False
        for letter in cleaned:
            if not (letter.isalnum() or letter == " "):
                return False
        return True

    @field_validator("player", mode="before")
    @classmethod
    def validate_player(cls, value: Any) -> str:
        """Validate a player name, substituting a default when invalid.

        Args:
            value: Unvalidated player name.

        Returns:
            The accepted name or the default player name.
        """
        if not isinstance(value, str):
            logger.warning(
                f"Invalid player_name '{value}'. Must be a string "
                "caracteres. Clamped to default: player1")
            return "player_1"
        if not cls._handle_player_names(value):
            logger.warning(
                "You not supposed to be here ! "
                f"Invalid player_name '{value}'. Numbers of caracteres < 11 "
                "Clamped to default: player1")
            return "player_1"
        return value

    @field_validator("score", mode="before")
    @classmethod
    def validate_score(cls, value: Any) -> int:
        """Validate a score and replace values outside the allowed range.

        Args:
            value: Unvalidated score.

        Returns:
            The score or zero when it is invalid.
        """
        if not isinstance(value, int) or value < 0 or value > 999999999:
            logger.warning(
                "You not supposed to be here ! "
                f"Invalid score '{value}'."
                " Clamped to default: 0")
            return 0
        return value


class HighScores(BaseModel):
    """Validated collection of high-score records."""

    scores: list[HighScore]
