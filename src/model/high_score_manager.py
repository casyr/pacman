import logging
from pathlib import Path
from pydantic import ValidationError

from model.high_score_validator import HighScore, HighScores
from utils.file_loader_json import JsonModelLoader
from exceptions import JsonLoadError

logger = logging.getLogger(__name__)


class HighScoreManager:
    def __init__(self, json: JsonModelLoader):
        self.json_loader = json
        self.file_path = Path(self.json_loader.file)
        self.scores: list[HighScore] = self.load_score()

    def handle_player_names(slef, player: str) -> bool:
        if len(player) > 10:
            return False
        for letter in player:
            if not (letter.isalnum() or letter == " "):
                return False
        return True

    def maj_score(
            self,
            scores: list[dict[str, str | int]],
            new_game: dict[str, str | int],
            ) -> list[HighScores]:

        new_score_model = HighScore.model_validate(new_game)
        self.scores.append(new_score_model)
        self.scores.sort(key=lambda item: item.score, reverse=True)
        self.scores = self.scores[:10]
        self.save_scores()
        return self.scores

    def save_scores(self) -> None:
        data_to_save = HighScores(scores=self.scores).model_dump()
        self.json_loader.save_json_file(self.file_path, data_to_save)

    def _reset_corrupted_file(self, reason: str) -> list:
        logger.warning(
            "The score file '%s' is invalid (%s). Resetting.",
            self.file_path,
            reason,
        )
        empty_data = {"scores": []}
        try:
            self.json_loader.save_json_file(self.file_path, empty_data)
        except JsonLoadError as e:
            logger.error("Unable to reset score file: %s", e)
        return []

    def load_score(self) -> list[HighScores]:
        if not self.file_path.exists():
            return self._reset_corrupted_file("Missing file")

        try:
            raw_content = self.json_loader.open_json_file(self.file_path)
        except Exception as e:
            return self._reset_corrupted_file(f"Reading error: {e}")

        try:
            validated_data = HighScores.model_validate_json(raw_content)
            validated_data.scores.sort(key=lambda item: item.score, reverse=True)
            return validated_data.scores[:10]
        except (ValidationError, Exception) as e:
            return self._reset_corrupted_file(f"Corupts file: {e}")
