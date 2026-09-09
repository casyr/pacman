import logging
from pathlib import Path
from ..model import HighScores
from ..errors import JsonLoadError

logger = logging.getLogger(__name__)


class JsonModelLoader:
    def __init__(self, file: str):
        self.file = file

    def save_json_file(
            self,
            file_name: Path,
            results: HighScores) -> None:
        folder_path = Path("data")
        file_path = folder_path / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(file_path, "w", encoding="utf-8") as output_file:
                json_string = results.model_dump_json(indent=4)
                output_file.write(json_string)
        except OSError as e:
            raise JsonLoadError(
                f" {file_path} could not save.") from e

    def check_json_exist(self) -> bool:
        file_path = Path(self.file)
        if not file_path.exists():
            file_path.touch()
            return False
        return True

    def check_json_format(self) -> Path:
        file_path = Path(self.file)
        if file_path.suffix.lower() != ".json":
            raise JsonLoadError("file must be a .json only !")
        return file_path

    def open_json_file(self, file_path: Path) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as text:
                raw_text = text.read()
                return raw_text
        except FileNotFoundError:
            raise JsonLoadError(f"File not found: '{file_path}'.")
        except PermissionError:
            raise JsonLoadError(f"Permission reading denied: '{file_path}'.")
