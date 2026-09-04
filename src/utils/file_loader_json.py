from pathlib import Path


class JsonModelLoader:
    def __init__(self, error_cls: type[Exception], file: str):
        self.error_cls = error_cls
        self.file = file

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
