from yaml import safe_load
from ..errors import ViewError
from typing import Any
from pydantic import BaseModel, ValidationError
from .sprite_model import SpriteModel
from pygame import Surface
from numpy import ndarray


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
        self.sprite_sheet = Graphic.load_sprite(self.sprite_path)
        self.sprite_sheet = self.sprite_sheet.convert(self.dest_image)
        self.sprite_sheet_buffer = Graphic.to_buffer(self.sprite_sheet)
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

    def get_sprite_buffer(self, data: ndarray, pos_x: int, pos_y: int,
                          file_width: int, width: int, height: int
                          ) -> ndarray:
        sheet_2d = data.reshape(-1, file_width)
        
        # Le slicing se fait uniquement sur l'axe Y et l'axe X
        sprite_2d = sheet_2d[pos_y : pos_y + height, pos_x : pos_x + width]
    
        return sprite_2d

    def get_sprite(self, sprite_name: str) -> SpriteModel:
        try:
            Sprites.model_validate(self.sprite_dict)
            data = self.sprite_dict["sprites"][sprite_name]
            pos_x = data["x"]
            pos_y = data["y"]
            width = data["w"]
            height = data["h"]
            file_width = self._get_sprite_file_width()
            sprite_buffer = self.get_sprite_buffer(self.sprite_sheet_buffer,
                                                   pos_x, pos_y, file_width,
                                                   width, height)
            sprite = SpriteModel(
                    pos_x,
                    pos_y,
                    width,
                    height,
                    file_width,
                    sprite_name,
                    sprite_buffer
            )
            return (sprite)
        except ValidationError as e:
            raise ViewError(e.errors()[0]['msg'])
