import numpy as np
from ..parsing.sprite_sheet_manager import SpriteData


class DisplayerUtils:
    """Provide shared pixel-layout and sprite drawing helpers."""

    @staticmethod
    def _get_padding() -> int:
        """Return the fixed screen padding used around the maze.

        Returns:
            The padding in pixels.
        """
        return 260

    def get_tile_size_maze(self, obj_width: int, obj_height: int,
                           screen_width: int, screen_height: int) -> int:
        """Calculate a maze tile size that is divisible by three.

        Args:
            obj_width: Maze width in tiles.
            obj_height: Maze height in tiles.
            screen_width: Available screen width in pixels.
            screen_height: Available screen height in pixels.

        Returns:
            The tile size in pixels.
        """

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
                            sprite_data: SpriteData | None) -> None:
        """Scale and copy non-transparent sprite pixels into an image.

        Args:
            dest_image_buffer: Destination pixel buffer.
            dest_image_width: Width of the destination image.
            dest_x: Horizontal destination position.
            dest_y: Vertical destination position.
            dest_w: Destination sprite width.
            dest_h: Destination sprite height.
            sprite_data: Sprite to draw, if available.
        """

        if sprite_data is None:
            return

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
