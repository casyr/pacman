import pygame
from numpy import ndarray
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from ..model import GameSession
from .menu import BaseMenuView


class SessionView(BaseMenuView):

    def __init__(self,
                 width: int,
                 height: int,
                 window: pygame.Surface,
                 text_sprites: SpriteSheetsManager) -> None:

        super().__init__(width, height, window, text_sprites)

    def render(
            self,
            dest_image_buffer: ndarray,
            game_session: GameSession,
            ) -> None:

        size = 20
        score_str = f"SCORE {game_session.score}"
        lives_str = f"VIES {game_session.lives_remaining}"
        time_str = f"TEMPS {int(game_session.time_remaining)}"

        time_w = self._calculate_string_width(time_str, size)
        time_x = self.width - time_w - 20

        self._render_text(
            dest_image_buffer,
            current_y=20,
            text=score_str,
            size=size, start_x=20
        )
        self._render_text(
            dest_image_buffer,
            current_y=50,
            text=lives_str,
            size=size,
            start_x=20
        )
        self._render_text(
            dest_image_buffer,
            current_y=20,
            text=time_str,
            size=size,
            start_x=time_x
        )
