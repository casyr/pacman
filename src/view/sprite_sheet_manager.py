from yaml import safe_load
from ..errors import ViewError
from typing import Any
from pydantic import BaseModel, ValidationError
<<<<<<< HEAD
from pygame import Surface



class SpriteSheetError(ViewError):
    """
    This error type in inheritance to ViewError
    and raised his own error in case of:
        - fail to laod sprite data
        - malformed file
    """


class Sprite:

    pos_x: int
    pos_y: int
    width: int
    height: int
    file_width: int
    sprite_surface: Surface


=======
from .sprite_model import SpriteModel
from pygame import Surface


>>>>>>> 78-viewcreateblackpixeltransparency
class SpriteData(BaseModel):
    x: int
    y: int
    w: int
    h: int


class Sprites(BaseModel):
    sprite_width: int
    sprites: dict[str, SpriteData]


class SpriteSheetManager:

    def __init__(self, sprite_path: str, sprite_path_data: str,
                 dest_image: Surface):
        from . import Graphic
        self.sprite_path = sprite_path
        self.sprite_path_data = sprite_path_data
        self.sprite_dict: dict[str, Any] = {}
        self.graphic = Graphic()
        self.dest_image = dest_image
        self.sprite = Graphic.load_sprite(self.sprite_path)
        self._get_sprites_sheet_data()

    def _get_sprites_sheet_data(self) -> None:
        try:
            with open(self.sprite_path_data, "r") as data:
                self.sprite_dict = safe_load(data)
        except (FileNotFoundError) as e:
            raise ViewError(e)
        except (PermissionError) as e:
            raise ViewError(e)

    def _get_sprite_file_width(self) -> int:
        return int(self.sprite_dict["sprite_width"])

    def get_sprite(self, sprite_name: str) -> SpriteModel:
        try:
            Sprites.model_validate(self.sprite_dict)
            data = self.sprite_dict["sprites"][sprite_name]
            sprite_buffer = self.sprite.convert(self.dest_image)

            buffer = self.graphic.to_buffer(sprite_buffer)
            sprite = SpriteModel(
                    data["x"],
                    data["y"],
                    data["w"],
                    data["h"],
                    self._get_sprite_file_width(),
                    self.sprite,
                    sprite_name,
                    buffer
            )
            return (sprite)
        except ValidationError as e:
            raise ViewError(e.errors()[0]['msg'])
