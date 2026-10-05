import numpy as np
from ..parsing.sprite_sheet_manager import SpriteData


class DisplayerUtils:

    @staticmethod
    def _get_padding() -> int:
        return 260

    def get_tile_size_maze(self, obj_width: int, obj_height: int,
                           screen_width: int, screen_height: int) -> int:

        usable_width = screen_width - self._get_padding()
        usable_height = screen_height - self._get_padding()
        px_tile_width = usable_width // obj_width
        px_tile_height = usable_height // obj_height
        raw_size = min(px_tile_height, px_tile_width)
        tile_size = (raw_size // 3) * 3
        return max(tile_size, 3)

    def put_sprite_in_image(self, dest_image_buffer: np.ndarray,
                            dest_image_width: int,
                            dest_x: int, dest_y: int,
                            dest_w: int, dest_h: int,
                            sprite_data: SpriteData) -> None:

        x_gap = np.arange(dest_w)
        y_gap = np.arange(dest_h)

        src_x = (sprite_data.coords.w * x_gap) // dest_w
        src_y = (sprite_data.coords.h * y_gap) // dest_h

        sprite_pos_1d = ((src_y)[:, None] * sprite_data.coords.w
                         + src_x).ravel()
        image_pos_1d = ((dest_y + y_gap)[:, None] *
                        dest_image_width + (dest_x + x_gap)).ravel()

        sprite_pixels = sprite_data.buffer[sprite_pos_1d]

        mask = sprite_pixels != 0

        dest_image_buffer[image_pos_1d[mask]] = sprite_pixels[mask]
