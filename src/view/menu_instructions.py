import pygame
import numpy as np
from . import mlx_wrapper as mlx
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from .menu import BaseMenuView


class InstructionsView(BaseMenuView):

    def __init__(self,
                 width: int,
                 height: int,
                 window: pygame.Surface,
                 text_sprites: SpriteSheetsManager,) -> None:

        super().__init__(width, height, window, text_sprites)
        self.title_lines: list[str] = [
            "Controls Movement",
            "",
            "",
            "press   w   to move up",
            "press   d   to move right",
            "press   a   to move left",
            "press   s   to move up",
            "",
            "",
            "Game Rules",
            "",
            "The Objective is to navigate the maze and eat all the",
            "pac-gums on the board to achieve victory.",
            "",
            "Watch out for the ghosts your enemies patrolling the corridors!",
            "Each has its own artificial intelligence and pursuit behavior.",
            "If they touch you, you lose the game. Observe their movement",
            "",
            "Every pac-gum you eat increases your score.",
            "Try to get your name on the High Scores board!",
            "Superpacgum bigger dot can provide you the power to eat ghost",
            "and collect more points",
            "",
            "Cheat mode is implemented if you want",
            "",
            "",
            '',
            "press   1   to return main menu"]
        self.size_char_pixel: int = 35
        self.title_size_pixel: int = 35

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
            if line.startswith("press   1"):
                start_x += start_x - self.margin_pixel
            self._render_text(
                dest_image_buffer,
                current_y,
                line,
                self.title_size_pixel,
                start_x
            )
            current_y += self.title_size_pixel + (self.gap_pixel * 2)

        return current_y

    def _create_cache_menu(self) -> pygame.Surface:

        if self._cached_buffer_menu is None:

            self._cached_buffer_menu = mlx.new_image(
                self.width,
                self.height).convert_alpha()
            buffer = mlx.to_buffer(self._cached_buffer_menu)

            self._render_titles(buffer)

            del buffer
        return self._cached_buffer_menu

    def render(self) -> None:

        cached_image = self._create_cache_menu()
        mlx.blit_img(cached_image, self.window, (0, 0))
        mlx.update_window()
