import pygame
from numpy import ndarray
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from ..model import GameSession
from .menu import BaseMenuView


class SessionView(BaseMenuView):
    """Render score, lives, time, level, and control hints."""

    def __init__(self,
                 width: int,
                 height: int,
                 window: pygame.Surface,
                 text_sprites: SpriteSheetsManager) -> None:
        """Initialize the session HUD.

        Args:
            width: Display width in pixels.
            height: Display height in pixels.
            window: Surface associated with the view.
            text_sprites: Sprite sheet containing text characters.
        """

        self.size = 20
        super().__init__(width, height, window, text_sprites)

    def render_score(self, dest_image_buffer: ndarray,
                     game_session: GameSession,
                     ) -> None:
        """Draw the current score in the upper-right HUD.

        Args:
            dest_image_buffer: Destination pixel buffer.
            game_session: Session containing the current score.
        """
        score_str = f"SCORE {game_session.score}"
        score_x = self.width - self._calculate_string_width(
                    score_str, self.size) - self.margin_pixel
        self._render_text(dest_image_buffer,
                          20,
                          score_str,
                          self.size,
                          score_x)

    def render_lifes(self, dest_image_buffer: ndarray,
                     game_session: GameSession,
                     ) -> None:
        """Draw the remaining lives in the HUD.

        Args:
            dest_image_buffer: Destination pixel buffer.
            game_session: Session containing the remaining lives.
        """
        lives_str = f"LIFES {game_session.lives_remaining}"
        lifes_x = self.width - self._calculate_string_width(
            lives_str, self.size) - self.margin_pixel
        self._render_text(dest_image_buffer,
                          50,
                          lives_str,
                          self.size,
                          lifes_x)

    def render_time(self, dest_image_buffer: ndarray,
                    game_session: GameSession,
                    ) -> None:
        """Draw the remaining time in the HUD.

        Args:
            dest_image_buffer: Destination pixel buffer.
            game_session: Session containing the remaining time.
        """
        time_str = f"TIME {int(game_session.time_remaining)}"
        time_x = self.width - self._calculate_string_width(
            time_str, self.size) - self.margin_pixel
        self._render_text(dest_image_buffer,
                          80,
                          time_str,
                          self.size,
                          time_x)

    def render_level_id(self, dest_image_buffer: ndarray,
                        game_session: GameSession,
                        ) -> None:
        """Draw the current level number in the HUD.

        Args:
            dest_image_buffer: Destination pixel buffer.
            game_session: Session containing the current level index.
        """
        level_str = f"LEVEL {int(game_session.level_index + 1)}"
        level_x = self.width - self._calculate_string_width(
            level_str, self.size) - self.margin_pixel
        self._render_text(dest_image_buffer,
                          110,
                          level_str,
                          self.size,
                          level_x)

    def render_pause_hook(self, dest_image_buffer: ndarray
                          ) -> None:
        """Draw the pause-control hint.

        Args:
            dest_image_buffer: Destination pixel buffer.
        """
        pause_str = "PRESS P TO PAUSE GAME"
        pause_x = self.width - self._calculate_string_width(
            pause_str, self.size) - self.margin_pixel
        self._render_text_left(dest_image_buffer,
                               20,
                               pause_str,
                               self.size,
                               pause_x)

    def render_cheat_hook(self, dest_image_buffer: ndarray
                          ) -> None:
        """Draw the cheat-menu control hint.

        Args:
            dest_image_buffer: Destination pixel buffer.
        """
        cheat_str = "PRESS C TO CHEAT MENU"
        cheat_x = self.width - self._calculate_string_width(
            cheat_str, self.size) - self.margin_pixel
        self._render_text_left(dest_image_buffer,
                               50,
                               cheat_str,
                               self.size,
                               cheat_x)

    def render(
            self,
            dest_image_buffer: ndarray,
            game_session: GameSession,
            ) -> None:
        """Draw all session statistics and control hints.

        Args:
            dest_image_buffer: Destination pixel buffer.
            game_session: Session state to display.
        """

        self.render_score(dest_image_buffer, game_session)
        self.render_lifes(dest_image_buffer, game_session)
        self.render_time(dest_image_buffer, game_session)
        self.render_level_id(dest_image_buffer, game_session)
        self.render_pause_hook(dest_image_buffer)
        self.render_cheat_hook(dest_image_buffer)
