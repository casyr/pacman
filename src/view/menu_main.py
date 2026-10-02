import pygame
import numpy as np
from . import mlx_wrapper as mlx
from ..parsing.sprite_validator import SpriteData
from ..parsing.sprite_sheet_manager import SpriteSheetsManager


class Menu:

    def __init__(self,
                 width: int,
                 height: int,
                 window: pygame.Surface,
                 menu_sprites: SpriteSheetsManager,) -> None:

        self.width: int = width
        self.height: int = height
        self.window: pygame.Surface = window
        self.menu: SpriteSheetsManager = menu_sprites
        self._cached_buffer_menu: pygame.Surface | None = None
        self.name_sprite_menu: list[str] = [
            "menu_play",
            "menu_score",
            "menu_instruction",
            "menu_exit"
        ]
        self.padding_pixel: int = 20
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

    def _render_logo(self, dest_image_buffer: np.ndarray,
                     dest_img_width: int, dest_img_height: int) -> int:
        logo_name = "logo"
        logo_sprite = self.menu.sprites.get(logo_name, None)
        if logo_sprite is None:
            return 0
        logo_h = int(dest_img_height * 0.25)
        logo_y = self.margin_pixel

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

    def _calculate_total_menus_height(self) -> int:
        total_menu = len(self.name_sprite_menu)
        if total_menu == 0:
            return 0
        return self.padding_pixel * (total_menu - 1)

    def _render_menus(self,
                      dest_image_buffer: np.ndarray,
                      dest_img_width: int,
                      dest_img_height: int,
                      start_y: int) -> None:

        total_menu: int = len(self.name_sprite_menu)

        height_available = (
            dest_img_height - start_y - self.margin_pixel - (
                self.padding_pixel * (total_menu - 1))) // 2

        menu_h = height_available // total_menu
        total_menus_height = self._calculate_total_menus_height()
        current_y = start_y + (height_available - total_menus_height) // 2

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

            current_y += menu_h + self.padding_pixel

    def _create_cache_menu(
            self,
            dest_width: int,
            dest_height: int) -> pygame.Surface:

        if self._cached_buffer_menu is None:
            self._cached_buffer_menu = mlx.new_image(
                dest_width,
                dest_height).convert_alpha()
            buffer = mlx.to_buffer(self._cached_buffer_menu)
            dest_img_height = buffer.size // dest_width
            logo_h = self._render_logo(
                buffer, dest_width, dest_img_height)
            self._render_menus(
                buffer, dest_width, dest_img_height, logo_h)
            del buffer
        return self._cached_buffer_menu

    def render(self) -> None:

        cached_image = self._create_cache_menu(self.width, self.height)
        mlx.blit_img(cached_image, self.window, (0, 0))
        mlx.update_window()
