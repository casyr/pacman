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
        # return pygame.surfarray.pixels2d(sprite).T.ravel()
        if not (sprite.get_flags() & pygame.SRCALPHA):
            sprite = sprite.convert_alpha()

        # Création de vues NumPy directes sur la surface (pas de copie mémoire)
        rgb = pygame.surfarray.pixels3d(sprite)
        alpha = pygame.surfarray.pixels_alpha(sprite)

        # Masque booléen pour cibler les pixels strictement noirs (R=0, G=0, B=0)
        black_mask = (rgb[:, :, 0] == 0) & (rgb[:, :, 1] == 0) & (rgb[:, :, 2] == 0)

        # Passage de l'alpha à 0 (transparence totale) pour ces pixels
        alpha[black_mask] = 0

        # Suppression des références pour déverrouiller la surface Pygame
        del rgb, alpha

        # Conversion du buffer de la surface en un tableau NumPy 1D (uint8)
        return np.frombuffer(sprite.get_buffer(), dtype=np.uint8)

    @staticmethod
    def get_padding() -> int:
        return 500

    # @staticmethod
    # def set_black_transparency(img_buffer: np.ndarray, img_width: int) -> None:
    #     img_buffer.reshape(-1, img_width)
    #     mask = (img_buffer[:, :3] == [0, 0, 0]).all(axis=-1)
    #     img_buffer[mask, 3] = 0
    #     img_buffer.ravel()
