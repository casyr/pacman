import pygame
import numpy as np
from . import mlx_wrapper as mlx
from .menu import BaseMenuView
from ..parsing.sprite_sheet_manager import SpriteSheetsManager


class CheatView(BaseMenuView):

    def __init__(self,
                 width: int,
                 height: int,
                 window: pygame.Surface,
                 text_sprites: SpriteSheetsManager) -> None:

        super().__init__(width, height, window, text_sprites)
        self.title_lines: list[str] = [
            "CHEAT MODE"]
        self.lines: list[str] = [
            "press   1   to be invincible",
            "press   2   to freeze ghosts",
            "press   3   to speed up",
            "press   4   to add 1 live",
            "press   5   to skip level",
            "press   6   to add 100 points",
            "press   c   to return"]

        self.size_char_pixel: int = 25
        self.title_size_pixel: int = 60

    def _render_titles(
            self,
            dest_image_buffer: np.ndarray) -> int:
        current_y = self.margin_pixel
        for line in self.title_lines:
            self._render_text(
                dest_image_buffer,
                current_y,
                line,
                self.title_size_pixel
            )
            current_y += self.title_size_pixel + (self.gap_pixel * 2)

        return current_y

    def _render_lines(self,
                      dest_image_buffer: np.ndarray,
                      start_y: int) -> None:

        start_y += self.margin_pixel
        step = self.size_char_pixel + self.margin_pixel

        for line in self.lines:
            self._render_text(
                dest_image_buffer,
                start_y,
                line,
                self.size_char_pixel
            )
            start_y += step

    def _create_cache_menu(self) -> pygame.Surface:

        if self._cached_menu_image is None:

            self._cached_menu_image = mlx.new_image(
                self.width,
                self.height).convert_alpha()
            buffer = mlx.to_buffer(self._cached_menu_image)

            title_end_y = self._render_titles(buffer)
            self._render_lines(buffer, title_end_y)

            del buffer
        return self._cached_menu_image

    def render(self) -> None:

        cached_image = self._create_cache_menu()
        mlx.blit_img(cached_image, self.window, (0, 0))
        mlx.update_window()
