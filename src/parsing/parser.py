import logging
from pathlib import Path
from pydantic import ValidationError
from .game_validator import GameValidator
from .game_settings import GameSettings
from ..errors import ParserError, GameSettingsError
from ..utils.file_loader_json import JsonModelLoader

logger = logging.getLogger(__name__)


class ConfigParser:
    def __init__(self, args: list[str]):
        self.args = args

    def _remove_all_comments(self, raw_text: str) -> str:
        result: list[str] = []
        i = 0
        length = len(raw_text)

        while i < length:
            char = raw_text[i]
            next_char = raw_text[i + 1] if i + 1 < length else ''

            if char == '"':
                i = self._handle_string(raw_text, i, length, result)
            elif char == '/' and next_char == '*':
                i = self._handle_block_comment(raw_text, i, length)
            elif (char == '/' and next_char == '/') or char == '#':
                i = self._handle_single_comment(raw_text, i, length)
            else:
                result.append(char)
                i += 1
        return "".join(result)

    def _handle_string(
            self, raw_text: str,
            i: int, length: int, result: list[str]) -> int:
        result.append(raw_text[i])
        i += 1

        while i < length:
            char = raw_text[i]
            next_char = raw_text[i + 1] if i + 1 < length else ''

            result.append(char)
            if char == '\\' and next_char:
                result.append(next_char)
                i += 2
                continue

            if char == '"':
                return i + 1
            i += 1

        return i

    def _handle_block_comment(self, raw_text: str, i: int, length: int) -> int:
        i += 2

        while i < length:
            char = raw_text[i]
            next_char = raw_text[i + 1] if i + 1 < length else ''

            if char == '*' and next_char == '/':
                return i + 2
            i += 1

        return i

    def _handle_single_comment(
            self, raw_text: str, i: int, length: int) -> int:
        while i < length:
            char = raw_text[i]
            if char == '\n':
                return i
            i += 1
        return i

    def _check_args(self) -> None:
        if len(self.args) == 0:
            raise ParserError("Missing argument: please provide a JSON "
                              "configuration file.")
        if len(self.args) > 1:
            raise ParserError(f"Too many arguments: expected 1, "
                              f"received {len(self.args)}.")

    def load(self) -> GameSettings:
        self._check_args()
        parser_json = JsonModelLoader(
            error_cls=ParserError, file=self.args[0])
        file_path: Path = parser_json.check_json_format()
        raw_text: str = parser_json.open_json_file(file_path)
        clean_text = self._remove_all_comments(raw_text)
        try:
            valid_game_settings = GameValidator.model_validate_json(clean_text)
            game_config: GameSettings = valid_game_settings.to_dataclass()
            logger.debug(valid_game_settings)
            return game_config
        except ValidationError as e:
            errors = ", ".join([err["msg"] for err in e.errors()])
            raise GameSettingsError(f"Validation failed: {errors}")
