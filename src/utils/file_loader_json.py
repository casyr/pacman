import json
from pathlib import Path
from src.exceptions import JsonLoadError


class JsonModelLoader:
    def __init__(self, error_cls: type[Exception], file: str):
        self.error_cls = error_cls
        self.file = file

    def save_json_file(
            self,
            file_path: Path,
            results: list[dict[str, int | str]]) -> None:

        try:
            with open(file_path, "w", encoding="utf-8") as output_file:
                json.dump(results, output_file, indent=4, ensure_ascii=False)
        except OSError as e:
            raise JsonLoadError(
                f"file at {file_path} could not save.") from e

    def check_json_exist(self) -> None:
        file_path = Path(self.file)
        if not file_path.exists():
            file_path.touch()

    def check_json_format(self) -> Path:
        file_path = Path(self.file)
        if file_path.suffix.lower() != ".json":
            raise self.error_cls("file must be a .json only !")
        return file_path

    def open_json_file(self, file_path: Path) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as text:
                raw_text = text.read()
                return raw_text
        except FileNotFoundError:
            raise self.error_cls(f"File not found: '{file_path}'.")
        except PermissionError:
            raise self.error_cls(f"Permission reading denied: '{file_path}'.")
