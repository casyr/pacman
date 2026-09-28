from dataclasses import dataclass
from pygame import Surface
from numpy import ndarray


@dataclass
class SpriteModel:

    pos_x: int
    pos_y: int
    width: int
    height: int
    file_width: int
    sprite_name: str
    buffer: ndarray
