import logging
from pathlib import Path
from pydantic import ValidationError
from .game_validator import GameValidator
from .game_settings import GameSettings
from ..errors import GameSettingsError
from ..utils.file_loader_json import JsonModelLoader

logger = logging.getLogger(__name__)


class ConfigParser:
    """Load and validate game settings from a commented JSON file."""

    def __init__(self, config_file_path: str):
        """Store the path to the configuration file.

        Args:
            config_file_path: Path to the JSON configuration file.
        """
        self.config_file_path = config_file_path

    def _remove_all_comments(self, raw_text: str) -> str:
        """Remove supported comments while preserving quoted strings.

        Args:
            raw_text: Source text that may contain comments.

        Returns:
            The source text with comments removed.
        """
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
        """Copy a quoted string and return the next source index.

        Args:
            raw_text: Source text being scanned.
            i: Index of the opening quote.
            length: Length of the source text.
            result: Output characters collected so far.

        Returns:
            The index immediately after the string, or the end of the text.
        """
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

    def _handle_block_comment(
            self, raw_text: str, i: int, length: int) -> int:
        """Skip a block comment and return the next source index.

        Args:
            raw_text: Source text being scanned.
            i: Index of the comment's opening slash.
            length: Length of the source text.

        Returns:
            The index after the comment, or the end of the text.
        """
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
        """Skip a line comment and return its newline index.

        Args:
            raw_text: Source text being scanned.
            i: Index where the comment starts.
            length: Length of the source text.

        Returns:
            The newline index or the end of the text.
        """
        while i < length:
            char = raw_text[i]
            if char == '\n':
                return i
            i += 1
        return i

    def load(self) -> GameSettings:
        """Read, validate, and convert the game configuration.

        Returns:
            Validated game settings.
        """
        parser_json = JsonModelLoader(file=self.config_file_path)
        file_path: Path = parser_json.check_json_format()
        raw_text: str = parser_json.open_json_file(file_path)
        clean_text = self._remove_all_comments(raw_text)
        try:
            valid_game_settings = GameValidator.model_validate_json(clean_text)
            game_config: GameSettings = valid_game_settings.to_dataclass()
            return game_config
        except ValidationError as e:
            errors = ", ".join([err["msg"] for err in e.errors()])
            raise GameSettingsError(f"Validation failed: {errors}")
