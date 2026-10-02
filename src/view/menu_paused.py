import pygame
import numpy as np
from . import mlx_wrapper as mlx
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from .menu import BaseMenuView


class PausedView(BaseMenuView):

    def __init__(self,
                 width: int,
                 height: int,
                 window: pygame.Surface,
                 text_sprites: SpriteSheetsManager,) -> None:

        super().__init__(width, height, window, text_sprites)
        self.title_lines: list[str] = [
            "MENU PAUSED"]
        self.lines: list[str] = [
            "press   1   to replay",
            "press   2   to return main menu"]
        self.size_char_pixel: int = 35
        self.title_size_pixel: int = 100

    def _render_titles(
            self,
            dest_image_buffer: np.ndarray) -> int:
        max_width = max(
            self._calculate_string_width(line, self.title_size_pixel)
            for line in self.title_lines
        )
        current_y = 0 + self.margin_pixel
        start_x = (self.width - max_width) // 2
        for line in self.title_lines:
            self._render_text(
                dest_image_buffer,
                current_y,
                line,
                self.title_size_pixel,
                start_x
            )
            current_y += self.title_size_pixel + (self.gap_pixel * 2)

        return current_y

    def _render_lines(self,
                      dest_image_buffer: np.ndarray,
                      start_y: int) -> None:

        start_y += self.margin_pixel // 2

        for line in self.lines:
            self._render_text(
                dest_image_buffer,
                start_y,
                line,
                self.size_char_pixel
            )
            start_y += self.margin_pixel

    def _create_cache_menu(self) -> pygame.Surface:

        if self._cached_buffer_menu is None:

            self._cached_buffer_menu = mlx.new_image(
                self.width,
                self.height).convert_alpha()
            buffer = mlx.to_buffer(self._cached_buffer_menu)

            title_end_y = self._render_titles(buffer)
            self._render_lines(buffer, title_end_y)

            del buffer
        return self._cached_buffer_menu

    def render(self) -> None:

        cached_image = self._create_cache_menu()
        mlx.blit_img(cached_image, self.window, (0, 0))
        mlx.update_window()
