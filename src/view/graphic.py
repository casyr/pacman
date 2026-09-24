import pygame
from ..errors import ViewError
from .sprite_sheet_manager import SpriteModel
import numpy as np


class Graphic:

    @staticmethod
    def initialisation() -> None:
        pygame.init()

    @staticmethod
    def new_window(width: int, height: int) -> pygame.Surface:
        return (pygame.display.set_mode((width, height)))

    @staticmethod
    def quit_window() -> None:
        pygame.quit()

    @staticmethod
    def new_image(width: int, height: int) -> pygame.Surface:
        return (pygame.Surface((width, height)))

    @staticmethod
    def update_window() -> None:
        pygame.display.update()

    @staticmethod
    def blit_img(image: pygame.Surface, dest_screen: pygame.Surface,
                 coords: tuple[int, int]) -> None:
        dest_screen.blit(image, coords)

    @staticmethod
    def load_sprite(path: str) -> pygame.Surface:
        try:
            return (pygame.image.load(path))
        except FileNotFoundError as e:
            raise ViewError(e)
        except PermissionError as e:
            raise ViewError(e)

    @staticmethod
    def to_buffer(sprite: pygame.Surface) -> np.ndarray:
        return pygame.surfarray.pixels2d(sprite).T.ravel()

    @staticmethod
    def get_padding() -> int:
        return 500

    def get_usable_width(self, screen_width: int) -> int:
        padding = self.get_padding()
        return (screen_width - padding)

    def get_usable_height(self, screen_height: int) -> int:
        padding = self.get_padding()
        return (screen_height - padding)

    def get_tile_size(self, maze_width: int, maze_height: int,
                      screen_width: int, screen_height: int) -> int:

        usable_width = self.get_usable_width(screen_width)
        usable_height = self.get_usable_height(screen_height)
        px_tile_width = usable_width // maze_width
        px_tile_height = usable_height // maze_height
        return min(px_tile_height, px_tile_width)

    def put_sprite_in_image(self, dest_image_buffer: np.ndarray,
                            dest_image_width: int,
                            dest_x: int, dest_y: int,
                            dest_w: int, dest_h: int,
                            sprite_data: SpriteModel) -> None:

        x_gap = np.arange(dest_w)
        y_gap = np.arange(dest_h)

        src_x = (sprite_data.width * x_gap) // dest_w
        src_y = (sprite_data.width * y_gap) // dest_h

        offset_x = sprite_data.pos_x
        offset_y = sprite_data.pos_y

        sprite_pos_1d = ((offset_y + src_y)[:, None] * sprite_data.file_width
                         + (offset_x + src_x)).ravel()
        image_pos_1d = ((dest_y + y_gap)[:, None] * dest_image_width
                        + (dest_x + x_gap)).ravel()

        dest_image_buffer[image_pos_1d] = sprite_data.buffer[sprite_pos_1d]
