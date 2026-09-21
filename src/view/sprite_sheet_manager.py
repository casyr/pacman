from yaml import safe_load
from ..errors import SpriteSheetError, ViewError
from typing import Any
from pydantic import BaseModel, ValidationError
from .sprite_model import SpriteModel


class SpriteData(BaseModel):
    x: int
    y: int
    w: int
    h: int


class Sprites(BaseModel):
    sprite_width: int
    sprites: dict[str, SpriteData]


class SpriteSheetManager:

    def __init__(self, sprite_path: str, sprite_path_data: str):
        from . import Graphic
        self.sprite_path = sprite_path
        self.sprite_path_data = sprite_path_data
        self.sprite_dict: dict[str, Any] = {}
        try:
            self.sprite = Graphic.load_sprite(self.sprite_path)
        except ViewError as e:
            raise SpriteSheetError(e)
        self._get_sprites_sheet_data()

    def _get_sprites_sheet_data(self) -> None:
        try:
            with open(self.sprite_path_data, "r") as data:
                self.sprite_dict = safe_load(data)
        except (FileNotFoundError) as e:
            raise SpriteSheetError(e)
        except (PermissionError) as e:
            raise SpriteSheetError(e)

    def _get_sprite_file_width(self) -> int:
        return int(self.sprite_dict["sprite_width"])

    def get_sprite(self, sprite_name: str) -> SpriteModel:
        try:
            Sprites.model_validate(self.sprite_dict)
            data = self.sprite_dict["sprites"][sprite_name]
            sprite = SpriteModel(
                    data["x"],
                    data["y"],
                    data["w"],
                    data["h"],
                    self._get_sprite_file_width(),
                    self.sprite,
                    sprite_name
            )
            return (sprite)
        except ValidationError as e:
            raise SpriteSheetError(e.errors()[0]['msg'])
        except ViewError as e:
            raise SpriteSheetError(e)
