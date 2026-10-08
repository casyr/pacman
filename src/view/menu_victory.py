import pygame
from . import mlx_wrapper as mlx
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from .menu import BaseMenuView


class VictoryView(BaseMenuView):

    def __init__(self,
                 width: int,
                 height: int,
                 window: pygame.Surface,
                 text_sprites: SpriteSheetsManager,) -> None:

        super().__init__(width, height, window, text_sprites)
        self.logo_name: str = "victory"

    def render(self, score: int) -> None:
        image = mlx.new_image(self.width, self.height).convert_alpha()
        buffer = mlx.to_buffer(image)
        self._render_text(
            buffer, self.size_char_pixel, self.logo_name, self.margin_pixel)
        score_text = f"Your score is {score}"
        score_y = self.margin_pixel + self.size_char_pixel + 50
        self._render_text(
            buffer, score_y, score_text, self.size_char_pixel)
        del buffer
        mlx.blit_img(image, self.window, (0, 0))
        mlx.update_window()

    def render_enter_score(self, score: int, player_name: str) -> None:
        image = mlx.new_image(self.width, self.height).convert_alpha()
        buffer = mlx.to_buffer(image)
        self._render_text(
            buffer, self.size_char_pixel, self.logo_name, self.margin_pixel)
        score_text = f"Your score is {score}"
        score_y = self.margin_pixel + self.size_char_pixel + 50
        self._render_text(
            buffer, score_y, score_text, self.size_char_pixel)
        name_y = score_y + self.size_char_pixel + 50
        display_name = f"NAME {player_name} "
        self._render_text(buffer, name_y, display_name, self.size_char_pixel)
        del buffer
        mlx.blit_img(image, self.window, (0, 0))
        mlx.update_window()
