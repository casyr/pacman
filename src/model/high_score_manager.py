import logging
from pathlib import Path
from pydantic import ValidationError

from .high_score_validator import HighScore, HighScores
from ..utils import JsonModelLoader
from ..errors import JsonLoadError

logger = logging.getLogger(__name__)


class HighScoreManager:
    """Load, validate, store, and maintain the top ten high scores."""

    def __init__(self, json: JsonModelLoader):
        """Initialize score storage and load existing scores.

        Args:
            json: Loader used to read and write the score file.
        """
        self.json_loader = json
        self.file_path = Path(self.json_loader.highscore_file_path())
        self.scores: list[HighScore] = self.load_score()

    def handle_player_names(self, player: str) -> bool:
        """Validate a player name using the score model's rules.

        Args:
            player: Name to validate.

        Returns:
            Whether the name satisfies the validation rules.
        """
        return HighScore._handle_player_names(player)

    def update_score(self, player_name: str, score: int) -> list[HighScore]:
        """Add a score, retain the top ten, and persist the results.

        Args:
            player_name: Name associated with the score.
            score: Score value to add.

        Returns:
            The current high scores in descending score order.
        """
        new_score_model = HighScore(player=player_name, score=score)
        self.scores.append(new_score_model)
        self.scores.sort(key=lambda item: item.score, reverse=True)
        self.scores = self.scores[:10]
        self.save_scores()
        return self.scores

    def save_scores(self) -> None:
        """Serialize and save the current high scores."""
        data_to_save = HighScores(scores=self.scores)
        try:
            self.json_loader.score_save_json_file(self.file_path, data_to_save)
        except JsonLoadError:
            logger.error("Could not save.")

    def _reset_corrupted_file(self, reason: str) -> list[HighScore]:
        """Replace an invalid score file with an empty score list.

        Args:
            reason: Explanation for why the file could not be used.

        Returns:
            An empty list of high scores.
        """
        logger.warning(
            f"The score file {self.file_path} is {reason}. Resetting.")
        empty_data: HighScores = HighScores(scores=[])
        try:
            self.json_loader.score_save_json_file(self.file_path, empty_data)
        except JsonLoadError as e:
            logger.error("Unable to reset score_file: %s", e)
        return []

    def load_score(self) -> list[HighScore]:
        """Load and validate scores, resetting the file if invalid.

        Returns:
            Up to ten validated scores in descending score order.
        """
        if not self.file_path.exists():
            return self._reset_corrupted_file("Missing file")
        try:
            raw_content = self.json_loader.open_json_file(self.file_path)
        except (OSError, JsonLoadError) as e:
            return self._reset_corrupted_file(f"Reading error: {e}")
        try:
            validated_data = HighScores.model_validate_json(raw_content)
            validated_data.scores.sort(
                key=lambda item: item.score, reverse=True)
            self.scores = validated_data.scores[:10]
            self.save_scores()
            return self.scores
        except (ValidationError, Exception) as e:
            return self._reset_corrupted_file(f"Corrupts file: {e}")
