import logging
from yaml import safe_load, YAMLError
from pathlib import Path
from pydantic import ValidationError
from .sprite_validator import SpriteData
from ..errors import SpriteSheetError

logger = logging.getLogger(__name__)


class SpriteSheetManager:
    def __init__(self, directory: str | Path):
        self.data_dir = self._resolve_directory(directory)
        self.allowed_files: list[str] = [".yaml", ".bmp"]
        self.allowed_sprite_name: list[str] = ["maze", "entities"]
        self.target_files: list[Path] = []
        self.sprites: dict[str, SpriteData] = {}

    def _resolve_directory(self, directory: str | Path) -> Path:
        path = Path(directory)
        if path.exists():
            print()
            return path
        root_dir = Path(__file__).resolve().parent.parent.parent
        resolved_path = root_dir / directory
        print(resolved_path)
        return resolved_path

    def _discover_files(self) -> None:
        self.target_files = [
            path for path in self.data_dir.rglob("*")
            if path.suffix in self.allowed_files]

    def _map_images(self) -> dict[Path, Path]:
        images_map: dict[Path, Path] = {}
        for path in self.target_files:
            if path.suffix == ".bmp":
                images_map[path.parent] = path
        return images_map

    def processed_sprite(self) -> None:
        self._discover_files()
        images_map = self._map_images()

        for file_path in self.target_files:
            if file_path.suffix == ".yaml":
                associated_image = images_map.get(file_path.parent)
                self._get_sprites_sheet_data(file_path, associated_image)

    def _get_sprites_sheet_data(
            self, file_path: Path, image_path: Path | None) -> None:
        try:
            with open(file_path, "r", encoding="utf-8") as data:
                raw_config_yaml = safe_load(data)

            for sprite_key in self.allowed_sprite_name:
                if sprite_key in raw_config_yaml:
                    for name, coords in raw_config_yaml[sprite_key].items():
                        if image_path is None:
                            raise SpriteSheetError(
                                f"Image.bmp missing for {name}")
                        coords["image_path"] = image_path
                        self.sprites[name] = SpriteData.model_validate(coords)
        except (FileNotFoundError, PermissionError) as e:
            raise SpriteSheetError(e)
        except YAMLError as e:
            raise SpriteSheetError(f"Syntax YAML in '{file_path.name}' : {e}")
        except ValidationError as e:
            errors = e.errors()
            first_error = errors[0]
            field = ".".join(str(loc) for loc in first_error["loc"])
            message = first_error["msg"]
            raise SpriteSheetError((f"Errror : '{field}' {message}"))
