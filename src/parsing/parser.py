import logging
from pathlib import Path
from pydantic import ValidationError
from exceptions import ParserError, GameSettingsError
from parsing.game_validator import GameValidator
from parsing.game_settings import GameSettings
from utils.file_loader_json import JsonModelLoader

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
        return json_str

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
            pydantic_model = GameValidator.model_validate_json(clean_text)
            game_config: GameSettings = pydantic_model.to_dataclass()
            return game_config
        except ValidationError as e:
            errors = ", ".join([err["msg"] for err in e.errors()])
            raise GameSettingsError(f"Validation failed: {errors}")
