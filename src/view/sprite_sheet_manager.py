from yaml import safe_load
from ..errors import ViewError
from typing import Any
from pydantic import BaseModel, ValidationError
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
        self.sprite_path = sprite_path
        self.sprite_path_data = sprite_path_data
        self.sprite_dict: dict[str, Any] = {}
        self.get_sprites_sheet_data()

    def get_sprites_sheet_data(self) -> None:
        try:
            with open(self.sprite_path_data, "r") as data:
                self.sprite_dict = safe_load(data)
        except (FileNotFoundError) as e:
            raise SpriteSheetError(e)
        except (PermissionError) as e:
            raise SpriteSheetError(e)

    def get_sprite_file_width(self) -> int:
        return int(self.sprite_dict["sprite_width"])

    def get_sprite(self, sprite_name: str) -> Sprite:
        from . import Graphics
        try:
            Sprites.model_validate(self.sprite_dict)
            data = self.sprite_dict["sprites"][sprite_name]
            sprite = Sprite()
            sprite.pos_x = data["x"]
            sprite.pos_y = data["y"]
            sprite.width = data["w"]
            sprite.height = data["h"]
            sprite.sprite_surface = Graphics.load_sprite(self.sprite_path)
            sprite.file_width = self.get_sprite_file_width()
            return (sprite)
        except ValidationError as e:
            raise SpriteSheetError(e.errors()[0]['msg'])
        except ViewError as e:
            raise SpriteSheetError(e)


