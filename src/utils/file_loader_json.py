import logging
from pathlib import Path
from pydantic import BaseModel
from ..errors import JsonLoadError

logger = logging.getLogger(__name__)


class JsonModelLoader:
    """Load JSON model data and save high-score results."""

    def __init__(self, file: str):
        """Store the JSON filename used by this loader.

        Args:
            file: JSON filename or path.
        """
        self.file = file

    def score_save_json_file(
            self,
            file_name: Path,
            results: BaseModel) -> None:
        """Write model results to a file beneath the data directory.

        Args:
            file_name: Destination filename relative to the data directory.
            results: Pydantic model whose data should be saved.
        """
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
        """Create the configured file if absent and report prior existence.

        Returns:
            Whether the configured file already existed.
        """
        file_path = Path(self.file)
        if not file_path.exists():
            file_path.touch()
            return False
        return True

    def check_json_format(self) -> Path:
        """Check the configured path has a JSON suffix.

        Returns:
            The configured path.
        """
        file_path = Path(self.file)
        if file_path.suffix.lower() != ".json":
            raise JsonLoadError("file must be a .json only !")
        return file_path

    def open_json_file(self, file_path: Path) -> str:
        """Read a UTF-8 JSON file.

        Args:
            file_path: Path to the file to read.

        Returns:
            The file contents as text.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as text:
                raw_text = text.read()
                return raw_text
        except FileNotFoundError:
            raise JsonLoadError(f"File not found: '{file_path}'.")
        except PermissionError:
            raise JsonLoadError(f"Permission reading denied: '{file_path}'.")

    def highscore_file_path(self) -> Path:
        """Resolve the high-score path and create its parent directory.

        Returns:
            An absolute path for the high-score file.
        """
        raw_file = Path(self.file)
        if raw_file.is_absolute():
            return raw_file.resolve()
        project_root = Path(__file__).resolve().parent.parent.parent
        full_path = (project_root / "data" / raw_file).resolve()
        full_path.parent.mkdir(parents=True, exist_ok=True)
        return full_path
