import pygame
import numpy as np
from ..parsing.sprite_validator import SpriteData
from ..parsing.sprite_sheet_manager import SpriteSheetsManager


class HighScoresView:

    def __init__(self,
                 highscore_sprites: SpriteSheetsManager,
                 window: pygame.Surface,
                 width: int,
                 height: int):
        self.highscore = highscore_sprites
        self.width = width
        self.height = height
        self.window = window

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

    def _render_highscore_image(self, dest_image_buffer: np.ndarray,
                                dest_img_width: int, dest_img_height: int) -> int:
        logo_name = "high_score"
        logo_sprite = self.highscore.sprites.get(logo_name, None)
        if logo_sprite is None:
            return 0
        logo_h = int(dest_img_height * 0.35)
        logo_w = dest_img_width
        logo_x = 0
        logo_y = 0

        self.put_sprite_in_image(
            dest_image_buffer,
            dest_img_width,
            logo_x,
            logo_y,
            logo_w,
            logo_h,
            logo_sprite
        )

        return logo_h

    def _render_menus(self,
                      dest_image_buffer: np.ndarray,
                      dest_img_width: int,
                      dest_img_height: int,
                      start_y: int) -> None:
        padding = 20
        down_margin = 200

        total_menu: int = len()

        height_available = dest_img_height - start_y - down_margin - (
            padding * (total_menu - 1))

        menu_h = height_available // total_menu

        current_y = start_y + padding

        for menu in self.name_sprite_menu:
            menu_sprite = self.menu.sprites[menu]

            ratio = menu_sprite.coords.w / menu_sprite.coords.h
            menu_w = int(menu_h * ratio)

            menu_x = (dest_img_width - menu_w) // 2

            self.put_sprite_in_image(
                dest_image_buffer,
                dest_img_width,
                menu_x,
                current_y,
                menu_w,
                menu_h,
                menu_sprite
            )

            current_y += menu_h + padding

    def render(self, dest_image_buffer: np.ndarray,
               dest_img_width: int) -> None:

        dest_img_height = dest_image_buffer.size // dest_img_width
        logo_h = self._render_logo(
            dest_image_buffer, dest_img_width, dest_img_height)
        self._render_menus(
            dest_image_buffer, dest_img_width, dest_img_height, logo_h)
