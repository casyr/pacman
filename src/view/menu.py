import pygame
import numpy as np
from ..parsing.sprite_validator import SpriteData
from ..parsing.sprite_sheet_manager import SpriteSheetsManager


class BaseMenuView:
    def __init__(self,
                 width: int,
                 height: int,
                 window: pygame.Surface,
                 text_sprites: SpriteSheetsManager) -> None:
        self.width: int = width
        self.height: int = height
        self.window: pygame.Surface = window
        self.text: SpriteSheetsManager = text_sprites
        self._cached_buffer_menu: pygame.Surface | None = None

        self.size_char_pixel: int = 15
        self.gap_pixel: int = 2
        self.margin_pixel: int = 20

    def put_sprite_in_image(self, dest_image_buffer: np.ndarray,
                            dest_image_width: int,
                            dest_x: int, dest_y: int,
                            dest_w: int, dest_h: int,
                            sprite_data: SpriteData) -> None:

        x_gap = np.arange(dest_w)
        y_gap = np.arange(dest_h)

        src_x = (sprite_data.coords.w * x_gap) // dest_w
        src_y = (sprite_data.coords.h * y_gap) // dest_h

        sprite_pos_1d = ((src_y)[:, None] *
                         sprite_data.coords.w + src_x).ravel()
        image_pos_1d = ((dest_y + y_gap)[:, None] *
                        dest_image_width + (dest_x + x_gap)).ravel()

        sprite_pixels = sprite_data.buffer[sprite_pos_1d]
        mask = sprite_pixels != 0
        dest_image_buffer[image_pos_1d[mask]] = sprite_pixels[mask]

    def _calculate_string_width(self, text: str, size: int) -> int:
        total_w = 0
        for char in text:
            if char == " ":
                total_w += size // 2 + self.gap_pixel
                continue
            char_sprite = self.text.sprites.get(f"char_{char.upper()}")
            if char_sprite:
                ratio = char_sprite.coords.w / char_sprite.coords.h
                total_w += int(size * ratio) + self.gap_pixel
        return total_w

    def _render_single_char(
            self,
            dest_image_buffer: np.ndarray,
            char: str,
            current_x: int,
            current_y: int,
            size: int) -> int:
        if char == " ":
            return size // 2

        char_sprite = self.text.sprites.get(f"char_{char.upper()}")
        if char_sprite:
            ratio = char_sprite.coords.w / char_sprite.coords.h
            char_w = int(size * ratio)
            self.put_sprite_in_image(
                dest_image_buffer,
                self.width,
                current_x,
                current_y,
                char_w,
                size,
                char_sprite
            )
            return char_w
        return 0

    def _render_text(
            self,
            dest_image_buffer: np.ndarray,
            current_y: int,
            text: str,
            size: int,
            start_x: int | None = None) -> None:

        if start_x is None:
            total_str_w = self._calculate_string_width(text, size)
            current_x = (self.width - total_str_w) // 2
        else:
            current_x = start_x

        for char in text:
            char_w = self._render_single_char(
                dest_image_buffer,
                char,
                current_x,
                current_y,
                size
            )
            current_x += char_w + self.gap_pixel
