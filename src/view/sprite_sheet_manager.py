from yaml import safe_load


class Sprite:

    pos_x: int
    pos_y: int
    width: int
    height: int
    path: str
    file_width: int


class SpriteSheet:

    def __init__(self, path: str):
        self.path = path
        with open("sprites/pacman_sprites.yaml", "r") as data:
            self.sprite_dict = safe_load(data)
        print(self.sprite_dict)

    def get_sprite_file_width(self) -> int:
        return (int(self.sprite_dict["sprite_width"]))

    def sprite_fill_data(self, sprite_name: str) -> Sprite:
        data = self.sprite_dict["sprites"][sprite_name]
        sprite = Sprite()
        sprite.pos_x = data["x"]
        sprite.pos_y = data["y"]
        sprite.width = data["w"]
        sprite.height = data["h"]
        sprite.path = self.path
        sprite.file_width = self.get_sprite_file_width()
        return (sprite)

