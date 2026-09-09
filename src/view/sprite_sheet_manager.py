import pyyaml
from .graphics import Graphics

class Sprite:

    pos_x: int
    pos_y: int
    width: int
    height: int


class SpriteSheetManager:

    def __init__(self):
        self.sprite_dict = pyyaml.dump.load("sprites/text_sprites.yaml")

    def get_sprite(self, sprite_name: str) -> Sprite:
        data = self.sprite_dict.get(sprite_name)
        sprite = Sprite()
        sprite.pos_x = data["x"]
        sprite.pos_y = data["y"]
        sprite.width = data["w"]
        sprite.height = data["h"]
        return (sprite)

    def get_sprite_file_width(path: str) -> int:
        img = Graphics().load_sprite(path)
        return (py)

