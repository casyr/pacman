import logging
from pathlib import Path
from exceptions import ParserError, GameSettingsError
from parsing.game_validator import GameSettings
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class ConfigParser:
    def __init__(self, args: list[str]):
        self.args = args

    def _remove_all_comments(self, raw_text: str) -> str:
        result: list[str] = []
        in_string = False
        in_comment = False
        in_comment_hash = False

        i = 0
        length = len(raw_text)

        while i != length:
            char = raw_text[i]
            if in_string:
                if char == '"':
                    in_string = False
                else:
                    result.append(char)
            elif in_comment:
                if char == '*' and i + 1 < length and raw_text[i+1] == '/':
                    in_comment = False
                    i += 1
                elif char == '/' and i + 1 < length and raw_text[i+1] == '/':
                    in_comment = False
                    i += 1
            elif in_comment_hash:
                if char == '\n':
                    in_comment_hash = False
            else:
                if char == '/' and i + 1 < length and raw_text[i+1] == '*':
                    in_comment = True
                    i += 1
                elif char == '/' and i + 1 < length and raw_text[i+1] == '/':
                    in_comment = True
                    i += 1
                elif char == '#':
                    in_comment_hash = True
                else:
                    result.append(char)
            i += 1
        json_str = "".join(result)
        logger.debug(json_str)
        return json_str

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
            with open(file_path, "r", encoding="utf-8") as text:
                raw_text = text.read()
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
