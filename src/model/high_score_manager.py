import logging
from pathlib import Path
from pydantic import ValidationError

from .high_score_validator import HighScore, HighScores
from ..utils import JsonModelLoader
from ..errors import JsonLoadError

logger = logging.getLogger(__name__)


class HighScoreManager:

    def __init__(self, json: JsonModelLoader):
        self.json_loader = json
        self.file_path = Path(self.json_loader.file)
        self.scores: list[HighScore] = self.load_score()

    def handle_player_names(self, player: str) -> bool:
        return HighScore._handle_player_names(player)

    def update_score(self, player_name: str, score: int) -> list[HighScore]:
        new_score_model = HighScore(player=player_name, score=score)
        self.scores.append(new_score_model)
        self.scores.sort(key=lambda item: item.score, reverse=True)
        self.scores = self.scores[:10]
        self.save_scores()
        return self.scores

    def save_scores(self) -> None:
        data_to_save = HighScores(scores=self.scores)
        try:
            self.json_loader.save_json_file(self.file_path, data_to_save)
        except JsonLoadError:
            logger.error("Check disk space.")

    def _reset_corrupted_file(self, reason: str) -> list:
        logger.warning(
            f"The score file {self.file_path} is {reason}. Resetting.")
        empty_data: HighScores = HighScores(scores=[])
        try:
            self.json_loader.save_json_file(self.file_path, empty_data)
        except JsonLoadError as e:
            logger.error("Unable to reset score_file: %s", e)
        return []

    def load_score(self) -> list[HighScore]:
        if not self.file_path.exists():
            return self._reset_corrupted_file("Missing file")
        try:
            raw_content = self.json_loader.open_json_file(self.file_path)
        except OSError as e:
            return self._reset_corrupted_file(f"Reading error: {e}")
        try:
            validated_data = HighScores.model_validate_json(raw_content)
            validated_data.scores.sort(
                key=lambda item: item.score, reverse=True)
            return validated_data.scores[:10]
        except (ValidationError, Exception) as e:
            return self._reset_corrupted_file(f"Corupts file: {e}")
