from high_score_validator import HightScoreValidator
from utils.file_loader_json import JsonModelLoader
from pydantic import ValidationError


class HighScoreManager:
    def __init__(self, json: JsonModelLoader, filename_score: str):
        self.json_loader: JsonModelLoader = json
        self.path_filename_score = self.load_score(filename_score)

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
            ) -> list[dict[str, str | int]]:

        scores.append(new_game)
        scores.sort(key=lambda item: int(item["score"]), reverse=True)

        return scores[:10]

    def load_score(self, filename_score: str) -> str:
        try:
            self.json_loader.check_json_exist(filename_score)
        except (PermissionError, FileNotFoundError):
            ## creat blank file 
        try:
            validate_scores = HightScoreValidator.model_validate_json(
                old_score)
            format_scores: list[dict[str, str | int]] = [score.model_dump() for score in validate_scores]
            return validate_scores
        except ValidationError as e:
            errors = ", ".join([err["msg"] for err in e.errors()])
            raise HightScoreValidator(f"Validation failed: {errors}")
        return format_scores
