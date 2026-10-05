import logging
from yaml import safe_load, YAMLError
from pathlib import Path
from pydantic import ValidationError
from .sprite_validator import (
    SpriteData,
    AnimationConfig,
    AnimationYamlConfig,
    SpriteSheetYamlConfig
)
from ..errors import SpriteSheetError
from ..view import mlx_wrapper
from numpy import ndarray


logger = logging.getLogger(__name__)


class SpriteSheetsManager:
    def __init__(self, directory: str | Path):
        self.data_dir = self._resolve_directory(directory)
        self.allowed_files: list[str] = [".yaml", ".bmp"]
        self.target_files: list[Path] = []
        self.sprites: dict[str, SpriteData] = {}
        self.animations: dict[str, AnimationConfig] = {}

    def _resolve_directory(self, directory: str | Path) -> Path:
        path = Path(directory)
        if path.exists():
            return path
        root_dir = Path(__file__).resolve().parent.parent.parent
        resolved_path = root_dir / directory
        return resolved_path

    def _discover_files(self) -> None:
        self.target_files = [
            path for path in self.data_dir.rglob("*")
            if path.suffix in self.allowed_files]

    def _map_images(self) -> dict[Path, Path]:
        images_map: dict[Path, Path] = {}
        for image_path in self.target_files:
            if image_path.suffix == ".bmp":
                images_map[image_path.parent] = image_path
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
        if image_path is None:
            raise SpriteSheetError(f"Image .bmp missing for {file_path.name}")
        try:
            with open(file_path, "r", encoding="utf-8") as data:
                raw_config_yaml = safe_load(data)
            config_yaml = SpriteSheetYamlConfig.model_validate(raw_config_yaml)

            sprite_sheet = mlx_wrapper.load_sprite(image_path)
            sprite_sheet_buffer = mlx_wrapper.to_buffer(sprite_sheet)

            self._load_static_sprites(config_yaml, sprite_sheet_buffer)
            self._load_animations(raw_config_yaml)

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

    def _load_static_sprites(
            self,
            config_yaml: SpriteSheetYamlConfig,
            sprite_sheet_buffer: ndarray) -> None:

        for sprite_name, coords in config_yaml.sprites.items():
            buffer = self.get_sprite_buffer(sprite_sheet_buffer,
                                            coords.x,
                                            coords.y,
                                            config_yaml.sprite_width,
                                            coords.w,
                                            coords.h)
            self.sprites[sprite_name] = SpriteData(
                sprite_width=config_yaml.sprite_width,
                coords=coords,
                buffer=buffer
            )

    def _load_animations(self, raw_config_yaml: dict) -> None:
        if "animations" not in raw_config_yaml:
            return
        raw_animations = raw_config_yaml["animations"]
        valid_animation = AnimationYamlConfig.model_validate(
            {"animations": raw_animations})
        for anim_name, anim_data in valid_animation.animations.items():
            if len(anim_data.frames) < 2:
                raise SpriteSheetError(
                    f"'{anim_name}' must contain at least 2 frames."
                    )
            self.animations[anim_name] = anim_data
