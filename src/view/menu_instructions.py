import pygame
import numpy as np
from . import mlx_wrapper as mlx
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from .menu import BaseMenuView


class InstructionsView(BaseMenuView):
    """Render instruction text loaded from the resource file."""

    def __init__(self,
                 width: int,
                 height: int,
                 window: pygame.Surface,
                 text_sprites: SpriteSheetsManager,) -> None:
        """Initialize the instruction screen.

        Args:
            width: Display width in pixels.
            height: Display height in pixels.
            window: Surface that receives the rendered instructions.
            text_sprites: Sprite sheet containing text characters.
        """

        super().__init__(width, height, window, text_sprites)
        self.title_lines: list[str] = self._load_instructions()
        self.title_size_pixel: int = 15
        self.margin_pixel: int = 20
        self.gap_pixel: int = 2

    def _load_instructions(self) -> list[str]:
        """Load instruction lines, returning a message if unavailable.

        Returns:
            The instruction lines or a missing-file message.
        """
        try:
            with open("sprites/text_sprites/instruction.txt", "r") as file:
                return [line.strip("\n") for line in file.readlines()]
        except FileNotFoundError:
            return ["Error: instructions.txt not found."]

    def _render_titles(
            self,
            dest_image_buffer: np.ndarray) -> int:
        """Draw instruction lines and return the next y position.

        Args:
            dest_image_buffer: Destination pixel buffer.

        Returns:
            The vertical position after the final instruction line.
        """

        current_y = self.margin_pixel
        step = 17
        for line in self.title_lines:
            self._render_text(
                dest_image_buffer,
                current_y,
                line,
                self.title_size_pixel
            )
            current_y += step

        return current_y

    def _create_cache_menu(self) -> pygame.Surface:
        """Create or return the cached instruction image.

        Returns:
            The cached instruction surface.
        """

        if self._cached_menu_image is None:

            self._cached_menu_image = mlx.new_image(
                self.width,
                self.height).convert_alpha()
            buffer = mlx.to_buffer(self._cached_menu_image)

            self._render_titles(buffer)

            del buffer
        return self._cached_menu_image

    def render(self) -> None:
        """Blit the instructions to the window and refresh it."""

        cached_image = self._create_cache_menu()
        mlx.blit_img(cached_image, self.window, (0, 0))
        mlx.update_window()
