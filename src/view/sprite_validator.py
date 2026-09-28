from pathlib import Path
from pydantic import BaseModel


class SpriteData(BaseModel):
    x: int
    y: int
    w: int
    h: int
    image_path: Path | None
