from dataclasses import dataclass
from pygame import Surface


@dataclass
class SpriteModel:

    pos_x: int
    pos_y: int
    width: int
    height: int
    file_width: int
    sprite_surface: Surface
    sprite_name: str
