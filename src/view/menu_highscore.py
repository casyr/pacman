import pygame
import numpy as np
from . import mlx_wrapper as mlx
from .menu import BaseMenuView
from ..model import HighScore
from ..parsing.sprite_sheet_manager import SpriteSheetsManager


class HighScoresView(BaseMenuView):

    def __init__(self,
                 width: int,
                 height: int,
                 window: pygame.Surface,
                 text_sprites: SpriteSheetsManager,) -> None:

        super().__init__(width, height, window, text_sprites)
        self.scores_in_session: list[HighScore] = []
        self.title_lines: list[str] = ["High", "Scores"]
        self.margin_pixel: int = 20
        self.gap_pixel: int = 2
        self.size_char_pixel: int = 15
        self.title_size_pixel: int = 25

    def _render_titles(
            self,
            dest_image_buffer: np.ndarray) -> int:

        current_y = 0 + self.margin_pixel

        for line in self.title_lines:
            self._render_text(
                dest_image_buffer,
                current_y,
                line,
                self.title_size_pixel
            )
            current_y += self.title_size_pixel + self.gap_pixel

        return current_y

    def _render_scores(self,
                       dest_image_buffer: np.ndarray,
                       start_y: int,
                       scores: list[HighScore]) -> int:

        total_scores = len(scores)
        if total_scores == 0:
            return start_y

        start_y += self.margin_pixel
        step = 30

        for score in scores:
            score_str = f"Player  {score.player}  score  {score.score}"
            self._render_text(
                dest_image_buffer,
                start_y,
                score_str,
                self.size_char_pixel
            )
            start_y += step
        return start_y

    def _render_play_instruction(self,
                                 dest_image_buffer: np.ndarray,
                                 start_y: int) -> int:

        start_y += self.margin_pixel
        play_str = "Press space to play or press 1 to return menu"
        self._render_text(
            dest_image_buffer,
            start_y,
            play_str,
            self.size_char_pixel
        )
        return start_y + self.margin_pixel

    def _create_cache_menu(
            self,
            scores: list[HighScore]) -> pygame.Surface:

        if (self.scores_in_session != scores or
                self._cached_menu_image is None):

            self._cached_menu_image = mlx.new_image(
                self.width,
                self.height).convert_alpha()
            buffer = mlx.to_buffer(self._cached_menu_image)

            title_end_y = self._render_titles(buffer)
            scores_end_y = self._render_scores(
                buffer,
                title_end_y,
                scores)
            self._render_play_instruction(buffer, scores_end_y)

            del buffer
            self.scores_in_session = scores
        return self._cached_menu_image

    def render(self,
               scores: list[HighScore]) -> None:

        cached_image = self._create_cache_menu(scores)
        mlx.blit_img(cached_image, self.window, (0, 0))
        mlx.update_window()
