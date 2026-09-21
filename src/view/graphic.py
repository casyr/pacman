import pygame
from ..errors import ViewError
from .sprite_sheet_manager import SpriteModel


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

    def get_scaling(self, maze_width: int, maze_height: int,
                    screen_width: int, screen_height: int) -> int:
        px_border_padding = 200
        usable_width = screen_width - px_border_padding
        usable_height = screen_height - px_border_padding
        px_tile_width = usable_width // maze_width
        px_tile_height = usable_height // maze_height
        if (px_tile_height < px_tile_width):
            tile_w_h = px_tile_height
        else:
            tile_w_h = px_tile_width
        print(tile_w_h // 24)
        return tile_w_h // 24

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
