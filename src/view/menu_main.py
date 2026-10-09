import pygame
import numpy as np
from . import mlx_wrapper as mlx
from ..parsing.sprite_sheet_manager import SpriteSheetsManager
from .menu import BaseMenuView
from ..errors import ViewError


class Menu(BaseMenuView):
    """Render the main menu and its logo."""

    def __init__(self,
                 width: int,
                 height: int,
                 window: pygame.Surface,
                 menu_sprites: SpriteSheetsManager,) -> None:
        """Initialize the main menu view.

        Args:
            width: Display width in pixels.
            height: Display height in pixels.
            window: Surface that receives the menu image.
            menu_sprites: Sprite sheet containing menu graphics.
        """

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
        """Draw the menu logo and return its vertical space.

        Args:
            dest_image_buffer: Destination pixel buffer.
            dest_img_width: Width of the destination image.
            dest_img_height: Height of the destination image.

        Returns:
            The y offset after the logo, or zero if it is absent.
        """
        logo_name = "logo"
        logo_sprite = self.menu.sprites.get(logo_name, None)
        if logo_sprite is None:
            return 0
        logo_h = int(dest_img_height * 0.15)
        logo_y = self.margin_pixel

        ratio = logo_sprite.coords.w / logo_sprite.coords.h
        logo_w = int(logo_h * ratio)
        logo_x = (dest_img_width - logo_w) // 2

        self.utils.put_sprite_in_image(
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
        """Draw each menu option below the logo.

        Args:
            dest_image_buffer: Destination pixel buffer.
            dest_img_width: Width of the destination image.
            dest_img_height: Height of the destination image.
            start_y: Vertical position at which menu options begin.
        """

        menu_h = int(dest_img_height * 0.05)
        current_y = start_y + self.padding_pixel

        for menu in self.name_sprite_menu:
            menu_sprite = self.menu.sprites[menu]

            ratio = menu_sprite.coords.w / menu_sprite.coords.h
            menu_w = int(menu_h * ratio)
            menu_x = (dest_img_width - menu_w) // 2

            self.utils.put_sprite_in_image(
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
        """Create or return the cached main-menu image.

        Args:
            dest_width: Image width in pixels.
            dest_height: Image height in pixels.

        Returns:
            The cached menu surface.
        """

        if self._cached_menu_image is None:
            self._cached_menu_image = mlx.new_image(
                dest_width,
                dest_height).convert_alpha()
            buffer = mlx.to_buffer(self._cached_menu_image)
            dest_img_height = buffer.size // dest_width
            logo_h = self._render_logo(
                buffer, dest_width, dest_img_height)
            try:
                self._render_menus(
                    buffer, dest_width, dest_img_height, logo_h)
                del buffer
            except KeyError as e:
                raise ViewError(f"menu_pacman.yaml file is invalid "
                                f"or is missing: {e}")
        return self._cached_menu_image

    def render(self) -> None:
        """Blit the main menu to the window and refresh it."""

        cached_image = self._create_cache_menu(self.width, self.height)
        mlx.blit_img(cached_image, self.window, (0, 0))
        mlx.update_window()
