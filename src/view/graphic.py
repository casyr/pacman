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

    # @staticmethod
    # def to_buffer(sprite: pygame.Surface) -> pygame.BufferProxy:
    #     return sprite.get_buffer()

    def get_padding(self):
        return 300

    def get_usable_width(self, screen_width: int) -> int:
        padding = self.get_padding()
        return (screen_width - padding)

    def get_usable_height(self, screen_height: int) -> int:
        padding = self.get_padding()
        return (screen_height - padding)

    def get_scaling(self, maze_width: int, maze_height: int,
                    screen_width: int, screen_height: int) -> int:

        usable_width = self.get_usable_width(screen_width)
        usable_height = self.get_usable_height(screen_height)

        px_tile_width = usable_width // maze_width
        px_tile_height = usable_height // maze_height
        if (px_tile_height < px_tile_width):
            tile_w_h = px_tile_height
        else:
            tile_w_h = px_tile_width
        return tile_w_h // 24

    def get_tile_size(self, maze_width: int, maze_height: int,
                           screen_width: int, screen_height: int) -> int:

        usable_width = self.get_usable_width(screen_width)
        usable_height = self.get_usable_height(screen_height)
        # print(f"{usable_height}\n, {usable_width}\n")
        px_tile_width = usable_width // maze_width
        px_tile_height = usable_height // maze_height
        return min(px_tile_height, px_tile_width)

    def put_sprite_in_image(self, dest_image: pygame.Surface,
                            dest_x: int, dest_y: int,
                            sprite_data: SpriteModel,
                            scaling: int) -> None:

        sprite = sprite_data.sprite_surface.convert(dest_image)

        sprite_buffer = pygame.surfarray.pixels2d(sprite).T.ravel()
        dest_image_buffer = pygame.surfarray.pixels2d(dest_image).T.ravel()

        dest_width = dest_image.get_width()

        scaled_w = sprite_data.width * scaling
        scaled_h = sprite_data.height * scaling

        for y_gap in range(scaled_h):
            for x_gap in range(scaled_w):
                src_x = sprite_data.pos_x + (x_gap // scaling)
                src_y = sprite_data.pos_y + (y_gap // scaling)
                sprite_pos = (src_y * sprite_data.file_width) + src_x
                image_pos = ((dest_y + y_gap) * dest_width) + (dest_x + x_gap)

                dest_image_buffer[image_pos] = sprite_buffer[sprite_pos]

    def put_sprite_in_image_(self, dest_image_buffer: np.ndarray,
                             dest_image_width: int,
                             dest_x: int, dest_y: int,
                             sprite_data: SpriteModel, maze_width: int,
                             maze_height: int) -> None:

        dest_tile_height = self.get_tile_size(maze_width, maze_height,
                                              dest_image_width,
                                              dest_image_width)

        src_file_w = sprite_data.file_width
        src_w = sprite_data.width  # Largeur du sprite source (ex: 8)
        src_h = sprite_data.height  # Hauteur du sprite source (ex: 8)

        # 2. Produit en croix vectorisé pour obtenir les coordonnées locales 0 -> dest_tile_height
        x_gap = np.arange(dest_tile_height)
        y_gap = np.arange(dest_tile_height)

        # Coordonnées dans le sprite source (produit en croix)
        src_x = (x_gap * src_w // dest_tile_height).astype(np.int32)
        src_y = (y_gap * src_h // dest_tile_height).astype(np.int32)

        # 3. Calcul des indices 1D pour CHAQUE pixel de la sous-grille (via outer / broadcasting)
        # Formule 1D Source : src_y * src_w + src_x
        sprite_pos_1d = (src_y[:, None] * src_file_w + src_x).ravel()

        # Formule 1D Destination : (dest_y + y_gap) * dest_w + (dest_x + x_gap)
        y_dest_global = dest_y + y_gap
        x_dest_global = dest_x + x_gap
        image_pos_1d = (y_dest_global[:, None] * dest_image_width + x_dest_global).ravel()

        # 4. Copie 1D instantanée exécutée en C
        dest_image_buffer[image_pos_1d] = sprite_data.buffer[sprite_pos_1d]
