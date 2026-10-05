import pygame
import numpy as np
from . import mlx_wrapper as mlx
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from .menu import BaseMenuView


class Menu(BaseMenuView):

    def __init__(self,
                 width: int,
                 height: int,
                 window: pygame.Surface,
                 menu_sprites: SpriteSheetsManager,) -> None:

        super().__init__(width, height, window, menu_sprites)
        self.menu: SpriteSheetsManager = menu_sprites
        self.name_sprite_menu: list[str] = [
            "menu_play",
            "menu_score",
            "menu_instruction",
            "menu_exit"
        ]
        self.padding_pixel: int = 20
        self.margin_pixel: int = 20

    def _render_logo(self, dest_image_buffer: np.ndarray,
                     dest_img_width: int, dest_img_height: int) -> int:
        logo_name = "logo"
        logo_sprite = self.menu.sprites.get(logo_name, None)
        if logo_sprite is None:
            return 0
        logo_h = int(dest_img_height * 0.15)
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

    def _render_menus(self,
                      dest_image_buffer: np.ndarray,
                      dest_img_width: int,
                      dest_img_height: int,
                      start_y: int) -> None:

        menu_h = int(dest_img_height * 0.05)
        current_y = start_y + self.padding_pixel

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

        if self._cached_menu_image is None:
            self._cached_menu_image = mlx.new_image(
                dest_width,
                dest_height).convert_alpha()
            buffer = mlx.to_buffer(self._cached_menu_image)
            dest_img_height = buffer.size // dest_width
            logo_h = self._render_logo(
                buffer, dest_width, dest_img_height)
            self._render_menus(
                buffer, dest_width, dest_img_height, logo_h)
            del buffer
        return self._cached_menu_image

    def render(self) -> None:

        cached_image = self._create_cache_menu(self.width, self.height)
        mlx.blit_img(cached_image, self.window, (0, 0))
        mlx.update_window()
