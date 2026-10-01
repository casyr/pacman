import pygame
import numpy as np
from . import mlx_wrapper as mlx
from ..parsing.sprite_validator import SpriteData
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from ..model import HighScore


class HighScoresView:

    def __init__(self,
                 width: int,
                 height: int,
                 window: pygame.Surface,
                 highscore_sprites: SpriteSheetsManager,) -> None:

        self.highscore: SpriteSheetsManager = highscore_sprites
        self.width: int = width
        self.height: int = height
        self.window: pygame.Surface = window
        self.scores_in_session: list[HighScore] = []
        self._cached_buffer_menu: pygame.Surface | None = None
        self.size_char_pixel: int = 35
        self.gap_pixel: int = 5
        self.margin_pixel: int = 200

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

    def _render_highscore_image(
            self,
            dest_image_buffer: np.ndarray,
            dest_img_width: int,
            dest_img_height: int) -> int:

        logo_name = "high_score"
        logo_sprite = self.highscore.sprites.get(logo_name, None)
        if logo_sprite is None:
            return 0 + self.margin_pixel
        logo_h = int(dest_img_height * 0.16)
        logo_w = dest_img_width
        logo_x = 0
        logo_y = 0 + self.margin_pixel

        ratio = logo_sprite.coords.w / logo_sprite.coords.h
        logo_w = int(logo_h * ratio)

        logo_x = (dest_img_width - logo_w) // 2

        self.put_sprite_in_image(
            dest_image_buffer,
            dest_img_width,
            logo_x,
            logo_y,
            logo_w,
            logo_h,
            logo_sprite
        )

        return logo_h + self.margin_pixel

    def _calculate_string_width(
            self,
            text: str) -> int:

        total_w = 0
        for char in text:
            if char == " ":
                total_w += self.size_char_pixel // 2 + self.gap_pixel
                continue
            char_sprite = self.highscore.sprites.get(f"char_{char.upper()}")
            if char_sprite:
                ratio = char_sprite.coords.w / char_sprite.coords.h
                total_w += int(self.size_char_pixel * ratio) + self.gap_pixel
        return total_w

    def _render_single_char(
            self,
            dest_image_buffer: np.ndarray,
            dest_img_width: int,
            char: str,
            current_x: int,
            current_y: int) -> int:

        if char == " ":
            return self.size_char_pixel // 2

        char_sprite = self.highscore.sprites.get(f"char_{char.upper()}")
        if char_sprite:
            ratio = char_sprite.coords.w / char_sprite.coords.h
            char_w = int(self.size_char_pixel * ratio)
            self.put_sprite_in_image(
                dest_image_buffer,
                dest_img_width,
                current_x,
                current_y,
                char_w,
                self.size_char_pixel,
                char_sprite
            )
            return char_w
        return 0

    def _render_score_line(
            self,
            dest_image_buffer: np.ndarray,
            dest_img_width: int,
            dest_img_height: int,
            score_str: str,
            current_y: int) -> None:

        total_str_w = self._calculate_string_width(score_str)
        current_x = (dest_img_width - total_str_w) // 2
        current_y = dest_img_height - current_y - self.margin_pixel
        for char in score_str:
            char_w = self._render_single_char(
                dest_image_buffer,
                dest_img_width,
                char,
                current_x,
                current_y
            )
            current_x += char_w + self.gap_pixel

    def _render_scores(self,
                       dest_image_buffer: np.ndarray,
                       dest_img_width: int,
                       dest_img_height: int,
                       start_y: int,
                       scores: list[HighScore]) -> None:

        total_scores = len(scores)
        if total_scores == 0:
            return

        for score in scores:
            score_str = f"Player : {score.player}  score : {score.score}"
            self._render_score_line(
                dest_image_buffer,
                dest_img_width,
                dest_img_height,
                score_str,
                start_y
            )
            start_y += self.margin_pixel

    def _create_cache_menu(
            self,
            dest_width: int,
            dest_height: int,
            scores: list[HighScore]) -> pygame.Surface:

        if (self.scores_in_session != scores or
                self._cached_buffer_menu is None):

            self._cached_buffer_menu = mlx.new_image(
                dest_width,
                dest_height).convert_alpha()
            buffer = mlx.to_buffer(self._cached_buffer_menu)
            dest_img_height = buffer.size // dest_width
            logo_h = self._render_highscore_image(
                buffer, dest_width, dest_img_height)
            self._render_scores(
                buffer,
                dest_width,
                dest_img_height,
                logo_h,
                scores)
            del buffer
            self.scores_in_session = scores
        return self._cached_buffer_menu

    def render(self,
               scores: list[HighScore]) -> None:

        cached_image = self._create_cache_menu(self.width, self.height, scores)
        mlx.blit_img(cached_image, self.window, (0, 0))
        mlx.update_window()
