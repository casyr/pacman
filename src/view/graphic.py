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
        # return pygame.surfarray.pixels2d(sprite).T.ravel()
        rgb = pygame.surfarray.pixels3d(sprite)
        alpha = pygame.surfarray.pixels_alpha(sprite)
    
        # 2. Masque pour rendre les pixels noirs transparents
        black_mask = (rgb[:, :, 0] == 0) & (rgb[:, :, 1] == 0) & (rgb[:, :, 2] == 0)
        alpha[black_mask] = 0
    
        # 3. Supprimer les références pour déverrouiller la surface
        del rgb, alpha
    
        # 4. Obtenir une vue 2D uint32 (1 élément = 1 pixel RGBA)
        # .T transpose (Width, Height) -> (Height, Width) pour correspondre au layout NumPy
        return pygame.surfarray.pixels2d(sprite).T.ravel()

    @staticmethod
    def get_padding() -> int:
        return 500

    # @staticmethod
    # def set_black_transparency(img_buffer: np.ndarray, img_width: int) -> None:
    #     img_buffer.reshape(-1, img_width)
    #     mask = (img_buffer[:, :3] == [0, 0, 0]).all(axis=-1)
    #     img_buffer[mask, 3] = 0
    #     img_buffer.ravel()
