from pydantic import BaseModel, ConfigDict, model_validator, Field
from typing import Any
from numpy import ndarray


class SpriteCoords(BaseModel):
    x: int
    y: int
    w: int
    h: int


class SpriteSheetYamlConfig(BaseModel):
    sprite_width: int
    category_name: str
    sprites: dict[str, SpriteCoords]

    @model_validator(mode='before')
    @classmethod
    def enforce_strict_structure(cls, data: dict[str, Any]) -> dict[str, Any]:
        keys = list(data.keys())

        if "sprite_width" not in keys:
            raise ValueError("Key 'sprite_width' missing")

        category_keys: list[str] = []
        for key in keys:
            if key not in ("sprite_width", "animation", "animations"):
                category_keys.append(key)

        if len(category_keys) != 1:
            raise ValueError("Main key missing (ex: 'maze', 'entities')")

        category_name = category_keys[0]

        return {
            "sprite_width": data["sprite_width"],
            "category_name": category_name,
            "sprites": data[category_name]
        }


class SpriteData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, strict=True)
    sprite_width: int
    coords: SpriteCoords
    buffer: ndarray


class AnimationConfig(BaseModel):
    speed: int
    loop: bool
    frames: list[str] = Field(min_length=2)


class AnimationYamlConfig(BaseModel):
    animations: dict[str, AnimationConfig]
