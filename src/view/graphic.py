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
        return 500

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
        src_w = sprite_data.width
        src_h = sprite_data.height

        x_gap = np.arange(dest_tile_height)
        y_gap = np.arange(dest_tile_height)

        src_x = (x_gap * src_w // dest_tile_height).astype(np.int32)
        src_y = (y_gap * src_h // dest_tile_height).astype(np.int32)

        src_x += sprite_data.pos_x
        src_y += sprite_data.pos_y

        sprite_pos_1d = (src_y[:, None] * src_file_w + src_x).ravel()

        y_dest_global = dest_y + y_gap
        x_dest_global = dest_x + x_gap
        image_pos_1d = (y_dest_global[:, None] * dest_image_width +
                        x_dest_global).ravel()

        dest_image_buffer[image_pos_1d] = sprite_data.buffer[sprite_pos_1d]

    def put_sprite_in_image_2(self, dest_image_buffer: np.ndarray,
                             dest_image_width: int,
                             dest_x: int, dest_y: int,
                             sprite_data: SpriteModel, maze_width: int,
                             maze_height: int) -> None:

        dest_tile_width = self.get_tile_size(maze_width, maze_height,
                                             dest_image_width,
                                             dest_image_width)

        print(dest_tile_width)
        dest_tile_height = dest_tile_width

        ratio = sprite_data.width / dest_tile_height

        for y_gap in range(dest_tile_height):
            for x_gap in range(dest_tile_height):
                src_x = int(ratio * x_gap)
                src_y = int(ratio * y_gap)
                sprite_pos = (src_y * sprite_data.file_width) + src_x
                image_pos = ((dest_y + y_gap) * dest_image_width) + (dest_x + x_gap)
                dest_image_buffer[image_pos] = sprite_data.buffer[sprite_pos]

    def put_sprite_in_image_3(self, dest_image_buffer: np.ndarray,
                              dest_image_width: int,
                              dest_x: int, dest_y: int,
                              dest_size: int,
                              sprite_data: SpriteModel) -> None:

        ratio = sprite_data.width / dest_size

        x_gap = np.arange(dest_size)
        y_gap = np.arange(dest_size)

        src_x = (ratio * x_gap).astype(np.int32)
        src_y = (ratio * y_gap).astype(np.int32)

        offset_x = sprite_data.pos_x
        offset_y = sprite_data.pos_y

        sprite_pos_1d = ((offset_y + src_y)[:, None] * sprite_data.file_width + (offset_x + src_x)).ravel()
        image_pos_1d = ((dest_y + y_gap)[:, None] * dest_image_width + (dest_x + x_gap)).ravel()

        dest_image_buffer[image_pos_1d] = sprite_data.buffer[sprite_pos_1d]
