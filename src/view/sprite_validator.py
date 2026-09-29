from pydantic import BaseModel, ConfigDict
from numpy import ndarray


class SpriteCoords(BaseModel):
    x: int
    y: int
    w: int
    h: int


class SpriteData(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True, strict = True)
    coords: SpriteCoords
    buffer: ndarray
