import logging
from pathlib import Path
from typing import TextIO
from exceptions import ParserError, GameSettingsError
from parsing.game_settings import GameSettings
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class ConfigParser:
    def __init__(self, args: list[str]):
        self.args = args

    def _remove_all_comments(self, raw_text: TextIO) -> str:
        result: list[str] = []
        for i, line in enumerate(raw_text):
            clean_line: str = line.strip()
            if clean_line == "" or clean_line.startswith("#"):
                continue
            clean_line_without_hash = clean_line.split("#")[0].strip()

        return "a"

    def _check_json_format(self) -> Path:
        file_path = Path(self.args[0])
        if file_path.suffix.lower() != ".json":
            raise ParserError("file must be a .json only !")
        return file_path

    def _check_args(self) -> None:
        if len(self.args) == 0:
            raise ParserError("Missing argument: please provide a JSON "
                              "configuration file.")
        if len(self.args) > 1:
            raise ParserError(f"Too many arguments: expected 1, "
                              f"received {len(self.args)}.")

    def load(self) -> GameSettings:
        self._check_args()
        file_path = self._check_json_format()
        try:
            with open(file_path, "r", encoding="utf-8") as raw_text:
                clean_text = self._remove_all_comments(raw_text)
                game_config = GameSettings.model_validate_json(clean_text)
                return game_config
        except FileNotFoundError:
            raise ParserError(f"File not found: '{file_path}'.")
        except PermissionError:
            raise ParserError(f"Permission reading denied: '{file_path}'.")
        except ValidationError as e:
            errors = ", ".join([err["msg"] for err in e.errors()])
            raise GameSettingsError(f"Validation failed: {errors}")
