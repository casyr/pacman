import pygame
from . import mlx_wrapper as mlx
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from .menu import BaseMenuView


class DefeatView(BaseMenuView):
    """Render the defeat screen and optional player name."""

    def __init__(self,
                 width: int,
                 height: int,
                 window: pygame.Surface,
                 text_sprites: SpriteSheetsManager,) -> None:
        """Initialize the defeat screen.

        Args:
            width: Display width in pixels.
            height: Display height in pixels.
            window: Surface that receives the rendered screen.
            text_sprites: Sprite sheet containing text characters.
        """

        super().__init__(width, height, window, text_sprites)
        self.logo_name: str = "defeat"

    def render(self, score: int) -> None:
        """Render the defeat message and final score.

        Args:
            score: Final score to display.
        """
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
        """Render the defeat message, score, and player name.

        Args:
            score: Final score to display.
            player_name: Player name to display.
        """
        image = mlx.new_image(self.width, self.height).convert_alpha()
        buffer = mlx.to_buffer(image)
        self._render_text(
            buffer, self.size_char_pixel, self.logo_name, self.margin_pixel)
        score_text = f"Your score is {score}"
        score_y = self.margin_pixel + self.size_char_pixel + 50
        self._render_text(
            buffer, score_y, score_text, self.size_char_pixel)
        name_y = score_y + self.size_char_pixel + 50
        display_name = f"NAME {player_name}"
        self._render_text(buffer, name_y, display_name, self.size_char_pixel)
        del buffer
        mlx.blit_img(image, self.window, (0, 0))
        mlx.update_window()
