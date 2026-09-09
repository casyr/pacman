import pyyaml


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

    def get_sprite_file_width(self, path: str) -> int:
        return (int(self.sprite_dict["sprite_width"]))
