import logging
from yaml import safe_load, YAMLError
from pathlib import Path
from pydantic import ValidationError
from .sprite_validator import SpriteData, SpriteCoords
from ..errors import SpriteSheetError
from . import mlx_wrapper
from numpy import ndarray


logger = logging.getLogger(__name__)


class SpriteSheetsManager:
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

    def get_sprite_buffer(self, data: ndarray, pos_x: int, pos_y: int,
                          file_width: int, width: int, height: int
                          ) -> ndarray:
        sheet_2d = data.reshape(-1, file_width)

        sprite_2d = sheet_2d[pos_y: pos_y + height, pos_x: pos_x + width]

        return sprite_2d.ravel()

    def _get_sprites_sheet_data(
            self, file_path: Path, image_path: Path | None) -> None:
        try:
            with open(file_path, "r", encoding="utf-8") as data:
                raw_config_yaml = safe_load(data)

            for sprite_key in self.allowed_sprite_name:

                if image_path is not None:
                    sprite_sheet = mlx_wrapper.load_sprite(image_path)
                    # sprite_sheet = mlx_wrapper.convert()
                    sprite_sheet_buffer = mlx_wrapper.to_buffer(sprite_sheet)

                if sprite_key in raw_config_yaml:

                    for name, coords in raw_config_yaml[sprite_key].items():
                        if image_path is None:
                            raise SpriteSheetError(
                                f"Image.bmp missing for {name}")
                        validate_coords = SpriteCoords.model_validate(coords)
                        print(validate_coords)
                        print(coords)
                        coords["buffer"] = self.get_sprite_buffer(sprite_sheet_buffer,
                                                                         coords["x"], coords["y"], 
                                                                         raw_config_yaml["sprite_width"],
                                                                         coords["w"], coords["h"])
                        self.sprites[name] = SpriteData.model_validate({"coords":coords, "buffer": coords["buffer"]})
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
