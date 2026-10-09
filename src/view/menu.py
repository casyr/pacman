import pygame
import numpy as np
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from .displayer_utils import DisplayerUtils
from ..errors import ViewError
import logging

logger = logging.getLogger(__name__)


class BaseMenuView:
    """Render text and shared menu elements into a window."""

    def __init__(self,
                 width: int,
                 height: int,
                 window: pygame.Surface,
                 text_sprites: SpriteSheetsManager) -> None:
        """Initialize shared menu rendering state.

        Args:
            width: Width of the display in pixels.
            height: Height of the display in pixels.
            window: Surface that receives rendered menu images.
            text_sprites: Sprite sheet containing text characters.
        """
        self.width: int = width
        self.height: int = height
        self.window: pygame.Surface = window
        self.text: SpriteSheetsManager = text_sprites
        self._cached_menu_image: pygame.Surface | None = None

        self.size_char_pixel: int = 15
        self.gap_pixel: int = 2
        self.margin_pixel: int = 20

        self.utils = DisplayerUtils()

    def _calculate_string_width(self, text: str, size: int) -> int:
        """Measure the rendered width of a string.

        Args:
            text: String to measure.
            size: Character height in pixels.

        Returns:
            The calculated width in pixels.
        """
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
        """Draw one character and return its rendered width.

        Args:
            dest_image_buffer: Pixel buffer to draw into.
            char: Character to render.
            current_x: Horizontal drawing position.
            current_y: Vertical drawing position.
            size: Character height in pixels.

        Returns:
            The rendered character width in pixels.
        """
        if char == " ":
            return size // 2

        char_sprite = self.text.sprites.get(f"char_{char.upper()}")
        try:
            if char_sprite is None:
                raise ViewError(f"Character '{char}' not found in sprites.")

            ratio = char_sprite.coords.w / char_sprite.coords.h
            char_w = int(size * ratio)
            self.utils.put_sprite_in_image(
                dest_image_buffer,
                self.width,
                current_x,
                current_y,
                char_w,
                size,
                char_sprite
            )
            return char_w
        except ViewError as e:
            logger.warning(f"Ignored character : {e}")
            return 0

    def _render_text(
            self,
            dest_image_buffer: np.ndarray,
            current_y: int,
            text: str,
            size: int,
            start_x: int | None = None) -> None:
        """Render text centered by default or from a given x position.

        Args:
            dest_image_buffer: Pixel buffer to draw into.
            current_y: Vertical drawing position.
            text: Text to render.
            size: Character height in pixels.
            start_x: Optional horizontal starting position.
        """

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

    def _render_text_left(
            self,
            dest_image_buffer: np.ndarray,
            current_y: int,
            text: str,
            size: int,
            start_x: int | None = None) -> None:
        """Render text from the left edge of the image buffer.

        Args:
            dest_image_buffer: Pixel buffer to draw into.
            current_y: Vertical drawing position.
            text: Text to render.
            size: Character height in pixels.
            start_x: Retained optional argument; currently unused.
        """

        current_x = 0

        for char in text:
            char_w = self._render_single_char(
                dest_image_buffer,
                char,
                current_x,
                current_y,
                size
            )
            current_x += char_w + self.gap_pixel
