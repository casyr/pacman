import pygame
from ..errors import ViewError
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
        return pygame.Surface((width, height), pygame.SRCALPHA)

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
        rgb = pygame.surfarray.pixels3d(sprite)
        alpha = pygame.surfarray.pixels_alpha(sprite)

        black_mask = ((rgb[:, :, 0] == 0)
                      & (rgb[:, :, 1] == 0)
                      & (rgb[:, :, 2] == 0))
        alpha[black_mask] = 0

        del rgb, alpha

        return pygame.surfarray.pixels2d(sprite).T.ravel()

    @staticmethod
    def get_padding() -> int:
        return 500
